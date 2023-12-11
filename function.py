import json
from bs4 import BeautifulSoup
import requests


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

                print ('link : {}'.format(link))
                print ('size : {}'.format(size))

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