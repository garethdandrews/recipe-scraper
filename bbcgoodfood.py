from bs4 import BeautifulSoup
import re

def get_recipe(soup):
    recipe = {}
    recipe['title'] = soup.find('h1').text

    # metadata (times, difficulty, servings)
    metadata = {}

    times_soup = soup.findAll('time')
    for item in times_soup:
        tmp = item.parent.previous_sibling.text[:-1]
        metadata[tmp] = item.text

    metadata['difficulty'] = soup.find(attrs={'class': 'masthead__skill-level'}).get_text()
    metadata['servings'] = soup.find(attrs={'class': 'masthead__servings'}).get_text()

    recipe['metadata'] = metadata

    # ingredients
    ingredient_list_soup = soup.find(['h2', 'h3'], text=re.compile("^ingredients$", re.I)).parent.findAll('section')

    ingredients = {}
    for section_soup in ingredient_list_soup:
        heading = section_soup.find('h3')
        heading = 'main' if heading is None else heading.text

        tmpList = []
        for item in section_soup.findAll('li'):
            tmpList.append(item.get_text())

        ingredients[heading] = tmpList

    recipe['ingredients'] = ingredients

    # method
    method_list_soup = soup.find(['h2', 'h3'], text=re.compile("^method$", re.I)).parent.findAll('li')

    method = []
    for item_soup in method_list_soup:
        method.append(item_soup.find('p').get_text())

    recipe['method'] = method

    return recipe