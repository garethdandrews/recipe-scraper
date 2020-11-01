import requests
from bs4 import BeautifulSoup

import bbcgoodfood

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent}

def get_content_from_url(url):
    response = requests.get(url, headers=headers, timeout=100)
    return BeautifulSoup(response.content, 'html.parser')



    
content = get_content_from_url('https://www.bbcgoodfood.com/recipes/old-delhi-style-butter-chicken')
bbcgoodfood.get_recipe(content)
