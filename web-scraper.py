from bs4 import BeautifulSoup
import requests

url = 'https://www.bbcgoodfood.com/recipes/next-level-spaghetti-bolognese/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent}

response = requests.get(url, headers=headers, timeout=100)
content = BeautifulSoup(response.content, "html.parser")

# recipe-header__title
title = content.findAll('h1', attrs={"class": "recipe-header__title"})
# print(title)

ingredients_list = content.findAll('li', attrs={"class": "ingredients-list__item"})

# for item in ingredients_list:
#     print(item)

print(ingredients_list[1]['content'])

# print(content)
# print(title[0].text)