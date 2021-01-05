from config import USER_AGENT
import requests
import time
from bs4 import BeautifulSoup

root_url = 'https://www.bbcgoodfood.com'

headers = {'User-Agent': USER_AGENT}

# uses the BeautifulSoup4 package to get the content of a webpage
def get_content_from_url(url):
    if root_url not in url:
        url = root_url + url
    response = requests.get(url, headers=headers, timeout=100)
    time.sleep(1)
    return BeautifulSoup(response.content, 'html.parser')
