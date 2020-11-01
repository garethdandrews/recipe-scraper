from bs4 import BeautifulSoup

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
                l = []
                for i in items:
                    l.append(i['content'])
                ingredients_array.append(l)
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