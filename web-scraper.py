from bs4 import BeautifulSoup
import requests
import time

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent}

def get_recipe_json(url, category):
    response = requests.get(url, headers=headers, timeout=100)
    content = BeautifulSoup(response.content, 'html.parser')

    title = content.find('h1', attrs={'class': 'recipe-header__title'}).text

    prep_time = content.find('span', attrs={'class': 'recipe-details__cooking-time-prep'})
    prep_time = prep_time.find('span').text

    cook_time = content.find('span', attrs={'class': 'recipe-details__cooking-time-cook'})
    cook_time = cook_time.find('span').text

    difficulty = content.find('section', attrs={'class': 'recipe-details__item recipe-details__item--skill-level'})
    difficulty = difficulty.find('span').text.strip()

    serves = content.find('section', attrs={'class': 'recipe-details__item recipe-details__item--servings'})
    serves = serves.find('span').text.strip()

    ingredients_list = content.findAll('li', attrs={'class': 'ingredients-list__item'})
    ingredients_array = []
    for item in ingredients_list:
        ingredients_array.append(item['content'])

    method = content.findAll('li', attrs={'class': 'method__item'})
    method_array = []
    for item in method:
        method_array.append(item.find('p').text)

    recipe = {
        'title': title,
        "category": category,
        'prepTime': prep_time,
        'cookTime': cook_time,
        'difficulty': difficulty,
        'serves': serves,
        'ingredients': ingredients_array,
        'method': method_array
    }

    return recipe

# url = 'https://www.bbcgoodfood.com/recipes/next-level-spaghetti-bolognese/'
# get_recipe_json('https://www.bbcgoodfood.com/recipes/next-level-spaghetti-bolognese')


def get_category_list(url):
    response = requests.get(url, headers=headers, timeout=100)
    content = BeautifulSoup(response.content, 'html.parser')

    categories = content.findAll('h3', attrs={'class': 'category-item--title'})

    category_list = []
    for item in categories:
        c = item.find('a')
        category_list.append({
            "name": c.text.strip(), 
            "url": "https://www.bbcgoodfood.com" + c['href']
        })

    return category_list


def get_recipe_list(category_list):
    for item in category_list:
        print(item)


url = "https://www.bbcgoodfood.com/recipes/category/dishes"
category_list = get_category_list(url)
time.sleep(5)

get_recipe_list(category_list)


