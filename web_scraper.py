import requests
import time
from bs4 import BeautifulSoup
import re
import bbcgoodfood

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


# starts the scraper to add recipes to the database
def start():
    bbcgoodfood.process_url('https://www.bbcgoodfood.com/recipes/category')


# starts the scraper to add tags to each recipe in the database
def start_tag_search():
    bbcgoodfood.process_url_for_tags('https://www.bbcgoodfood.com/recipes/category')

start_tag_search()