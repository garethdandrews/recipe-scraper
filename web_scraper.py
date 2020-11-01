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
def get_category_urls_from_dropdown(root_url):
    soup = get_content_from_url(root_url)
    recipes_soup = soup.find('span', attrs={'class': 'main-nav__nav-text'}, text=re.compile("^recipes$", re.I)).parent.next_sibling
    categories_soup = recipes_soup.findChildren('span', text='see more...')
    return [category_soup.parent.get('href') for category_soup in categories_soup]


# gets a list of collections from a category - 'collections' hold the list of recipes on bbcgoodfood
def get_collections_from_category(category_url):
    category_headings = get_content_from_url(category_url).findAll('h4')
    return [category_heading.find('a').get('href') for category_heading in category_headings]


lst = ['/recipes/category/all-vegetarian']

for category_url in lst:
    url = root_url + category_url

    collection_urls = []

    
    if 'category' in url:
        collection_urls.append(get_collections_from_category(url))
    else:
        collection_urls.append(url)
    



# content = get_content_from_url('https://www.bbcgoodfood.com/recipes/old-delhi-style-butter-chicken')
# bbcgoodfood.get_recipe(content)
