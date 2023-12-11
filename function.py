import json
from bs4 import BeautifulSoup
import requests

def scraping_bdm():

    url = 'https://www.blogdumoderateur.com/'
    response_bdm = requests.get(url)
    soup_bdb = BeautifulSoup(response_bdm.text)

    article_dict = {}
    articles = soup_bdb.find_all('article')

    for article in articles:
        id = article.get('id')

        title = article.find('h3').text.replace('\xa0', ' ')            # Title
        
        try:image = article.find('img')['data-lazy-src']                # Image
        except:image = None
       
        try:link = article.find('a')["href"]                            # Link
        except:link = article.parent['href']

        try:theme = article.find('span', 'favtag').text                 # CatÃ©gorie
        except:theme = article.find_previous('h2').text
        
        date = article.find('time')['datetime'].split('T')[0]           # Date
        
        article_dict[id] = { 'title' :title, 'date'  :date, 'link':link, 'image' :image, 'categorie' : theme }

    with open ('bdm.json', 'w') as f:json.dump(article_dict, f)
    return article_dict