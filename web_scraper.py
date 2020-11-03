import requests
import time
from bs4 import BeautifulSoup
import re

import bbcgoodfood

root_url = 'https://www.bbcgoodfood.com'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent}

def get_content_from_url(url):
    response = requests.get(url, headers=headers, timeout=100)
    time.sleep(1)
    return BeautifulSoup(response.content, 'html.parser')


# gets a list of category urls from the recipes dropdown box
def get_category_urls_from_dropdown():
    soup = get_content_from_url(root_url)
    recipes_soup = soup.find('span', attrs={'class': 'main-nav__nav-text'}, text=re.compile("^recipes$", re.I)).parent.next_sibling
    categories_soup = recipes_soup.findChildren('span', text='see more...')
    return [root_url + category_soup.parent.get('href') for category_soup in categories_soup]


# gets a list of collections from a category - 'collections' hold the list of recipes on bbcgoodfood
def get_collections_from_category(category_url):
    soup = get_content_from_url(category_url)
    collection_urls = [category_heading.find('a').get('href') for category_heading in soup.findAll('h4')]

    # check if there is more than one page in the category
    for url in get_pagination_urls(soup):
        soup = get_content_from_url(url)
        collection_urls = collection_urls + [category_heading.find('a').get('href') for category_heading in soup.findAll('h4')]

    return collection_urls
    

def get_pagination_urls(soup):
    pagination_items = soup.find('div', attrs={'pagination'})
    if pagination_items is None or len(pagination_items) is 1:
        return []
    pagination_items = pagination_items.findAll('a', attrs={'class': 'pagination-item'})
    return [root_url + item.get('href') for item in pagination_items]


category_urls = get_category_urls_from_dropdown()

collection_urls = []
for url in category_urls:
    collection_urls += get_collections_from_category(url)

print(collection_urls)
print(len(collection_urls))


