from bs4 import BeautifulSoup
import requests
import time

root_url = "https://www.bbcgoodfood.com"
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent}

def get_content_from_url(url):
    response = requests.get(url, headers=headers, timeout=100)
    return BeautifulSoup(response.content, 'html.parser')


def get_recipe_json(url, category):
    content = get_content_from_url(url)

    title = content.find('h1', attrs={'class': 'recipe-header__title'}).text

    prep_time = content.find('span', attrs={'class': 'recipe-details__cooking-time-prep'})
    if prep_time != None:
        prep_time = prep_time.find('span').text

    cook_time = content.find('span', attrs={'class': 'recipe-details__cooking-time-cook'})
    if cook_time != None:
        cook_time = cook_time.find('span').text

    full_time = content.find('span', attrs={'class': 'recipe-details__cooking-time-full'})
    if full_time != None:
        full_time = full_time.text

    difficulty = content.find('section', attrs={'class': 'recipe-details__item recipe-details__item--skill-level'})
    difficulty = difficulty.find('span').text.strip()

    serves = content.find('section', attrs={'class': 'recipe-details__item recipe-details__item--servings'})
    serves = serves.find('span').text.strip()

    ingredients_list_content = content.find('div', attrs={'class': 'ingredients-list__content'})
    ingredients_array = []
    for child in ingredients_list_content.contents:
        if child.name == 'ul':
            items = child.findAll('li', attrs={'class': 'ingredients-list__item'})
            if len(items) == 0:
                continue
            else:
                for i in items:
                    ingredients_array.append(i['content'])
        elif child.name == 'h3':
            ingredients_array.append(child.text)
        else:
            continue

    method = content.findAll('li', attrs={'class': 'method__item'})
    method_array = []
    for item in method:
        method_array.append(item.find('p').text)

    recipe = {
        'title': title,
        "category": category,
        'prepTime': prep_time,
        'cookTime': cook_time,
        'fullTime': full_time,
        'difficulty': difficulty,
        'serves': serves,
        'ingredients': ingredients_array,
        'method': method_array,
        'url': url
    }

    return recipe


def get_list(content):
    l = []
    for item in content:
        i = item.find('a')
        l.append({
            'name': i.text.strip(),
            'url': root_url + i['href']
        })
    return l


def get_category_list(url):
    content = get_content_from_url(url)

    categories = content.findAll('h3', attrs={'class': 'category-item--title'})
    return get_list(categories)


def get_recipes_from_content(content):
    return get_list(content.findAll('h3', attrs={'class': 'teaser-item__title'}))


def get_recipe_list(category_list):
    recipes = []
    for item in category_list:
        content = get_content_from_url(item['url'])
        recipes.append(get_recipes_from_content(content))
        time.sleep(1)   

        pages = content.findAll('li', attrs={'class': 'pager-item'})
        for page in pages[1:]:
            url = root_url + page.find('a')['href']
            content = get_content_from_url(url)
            recipes.append(get_recipes_from_content(content))
            time.sleep(1)

    print(recipes)



url = "https://www.bbcgoodfood.com/recipes/category/dishes"
# category_list = get_category_list(url)
# time.sleep(1)

# category_list = [{'name': 'Curry', 'url': 'https://www.bbcgoodfood.com/recipes/collection/curry'}]
# get_recipe_list(category_list)

get_recipe_json('https://www.bbcgoodfood.com/recipes/good-steak-kidney-pie', 'Pie')
