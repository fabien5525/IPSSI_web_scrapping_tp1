import json
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.by import By
from models.article import Article
from models.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pandas import DataFrame

def scraping_bdm(url):
    response_bdm = requests.get(url)
    soup_bdb = BeautifulSoup(response_bdm.content, 'html.parser')

    article_dict = {}
    articles = soup_bdb.find_all('article')

    for article in articles:
        id = article.get('id')

        title = article.find('h3').text.replace('\xa0', ' ')

        try:
            srcs = article.find('img').attrs['srcset'].split(',')

            selected_size = 0

            for src in srcs:

                src = src.strip()
                link = src.split(' ')[0]
                size = src.split(' ')[1]

                # size is in the format 123w
                size = int(size[:-1])

                if size > selected_size:
                    selected_size = size
                    image = link
        except:
            try:
                image = article.find('img')['src']
            except:
                pass

        try:
            link = article.find('a')["href"]                
        except:
            link = article.parent['href']

        theme = article.find('span', 'favtag').text

        date = article.find('time')['datetime'].split('T')[0]           # Date

        article_dict[id] = {'title': title, 'date': date,
                            'link': link, 'image': image, 'categorie': theme}

    with open('bdm.json', 'w') as f:
        json.dump(article_dict, f)
    return article_dict


def scraping_ldlc(driver, url):
    driver.get(url)

    data = {}

    products = driver.find_elements(By.XPATH, '//div[@class="listing-product"]/ul/li[not(ancestor::ul[@class="pagination"])]')

    for product in products:

        id = product.get_attribute('data-id')

        aTag = product.find_element(By.XPATH, './/div[@class="pdt-desc"]/h3/a')
        name = aTag.text

        imageTag = product.find_element(By.XPATH, './/div[@class="pic"]/a/img')
        image = imageTag.get_attribute('src')

        link = aTag.get_attribute('href')

        try : 
            priceTag = product.find_element(By.XPATH, './/div[@class="price"]/div[@class="price"]')
        except:
            priceTag = product.find_element(By.XPATH, './/div[@class="price"]/div[@class="new-price"]')
        
        priceInteger = priceTag.text.replace(' ', '').replace('&nbsp;', '').split('€')[0]
        priceDecimals = priceTag.find_element(By.XPATH, './/sup').text
        price = float(priceInteger + '.' + priceDecimals)

        note = None
        try:
            noteTag = product.find_element(By.XPATH, './/span[contains(@class, "star-")]')
            note = int(noteTag.get_attribute('class').split('-')[-1]) / 2
        except:
            pass

        data[id] = {
            'name': name,
            'image': image,
            'link': link,
            'price': price,
            'note': note
        }

    return data

def save_ldlc_data_to_db(df: DataFrame):
    engine = create_engine('sqlite:///sqlite.db', echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        for index, row in df.iterrows():
            # article : id_ldlc, name, image, link, price, note
            article = Article(
                index,
                row['name'],
                row['image'],
                row['link'],
                row['price'],
                row['note']
            )
            session.add(article)
        session.commit()

    engine.dispose()

def get_all_articles_from_db():
    engine = create_engine('sqlite:///sqlite.db', echo=True)
    Base.metadata.create_all(engine)

    data = {}

    with Session(engine) as session:
        articles = session.query(Article).all()
        session.commit()

        for article in articles:
            data[article.id_ldlc] = {
                'name': article.name,
                'image_link': article.image_link,
                'link': article.link,
                'price': article.price,
                'note': article.note
            }

    engine.dispose()

    return DataFrame.from_dict(data, orient='index')


def clear_articles():
    engine = create_engine('sqlite:///sqlite.db', echo=True)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        articles = session.query(Article).all()
        session.commit()

        for article in articles:
            session.delete(article)
        session.commit()

    engine.dispose()