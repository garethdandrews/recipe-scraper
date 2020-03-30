from bs4 import BeautifulSoup
import requests

url = 'https://www.bbcgoodfood.com/recipes/next-level-spaghetti-bolognese/'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent}

response = requests.get(url, headers=headers, timeout=100)
content = BeautifulSoup(response.content, "html.parser")

title = content.find('h1', attrs={"class": "recipe-header__title"}).text

ingredients_list = content.findAll('li', attrs={"class": "ingredients-list__item"})
ingredients_array = []
for item in ingredients_list:
    ingredients_array.append(item['content'])

method = content.findAll('li', attrs={"class": "method__item"})
method_array = []
for item in method:
    method_array.append(item.find('p').text)

recipe = {
    "title": title,
    "ingredients": ingredients_array,
    "method": method_array
}

print(recipe)