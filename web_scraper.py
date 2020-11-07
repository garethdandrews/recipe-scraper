import requests
import time
from bs4 import BeautifulSoup
import re

import bbcgoodfood
import recipe_repo

root_url = 'https://www.bbcgoodfood.com'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent}


# uses the BeautifulSoup4 package to get the content of a webpage
def get_content_from_url(url):
    if root_url not in url:
        url = root_url + url
    response = requests.get(url, headers=headers, timeout=100)
    time.sleep(1)
    return BeautifulSoup(response.content, 'html.parser')


# gets a list of urls from the headings of a page
def get_heading_urls(soup):
    return [title_soup.get('href') for title_soup in soup.findAll('a', attrs={'class': 'standard-card-new__article-title'})]


# gets a list of urls from the headings of all pages in a section
def get_headings_from_section(url):
    soup = get_content_from_url(url)
    pages_soup = [soup] + [get_content_from_url(page_url) for page_url in get_pagination_urls(soup)]
    heading_urls = []
    for page_soup in pages_soup:
        heading_urls += get_heading_urls(page_soup)
    return heading_urls


# gets a list of urls for the other pages in a category/collection that aren't currently selected 
# e.g. if on page 1 of 3, it will get the urls of pages 2 and 3
def get_pagination_urls(soup):
    pagination_items = soup.find('div', attrs={'pagination'})
    if pagination_items is None or len(pagination_items) is 1:
        return []
    pagination_items = pagination_items.findAll('a', attrs={'class': 'pagination-item'})
    return [item.get('href') for item in pagination_items]


# returns true if the url points to a category or a collection
def is_url_category_or_collection(url):
    return re.search("(?<=recipes\/)(category|collection)", url) is not None
    

# if a url is a category/collection, it gets the headings from those sections and checks again, until it finds a recipe
def process_url(url):
    if is_url_category_or_collection(url):
        [process_url(heading_url) for heading_url in get_headings_from_section(url)]
    else:
        soup = get_content_from_url(url)
        recipe = bbcgoodfood.get_recipe(soup)
        recipe_repo.insert_one(recipe)
        print("Added recipe: {0}".format(recipe['title']))


# starts the scraper
process_url('https://www.bbcgoodfood.com/recipes/category')
