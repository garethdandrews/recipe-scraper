from bs4 import BeautifulSoup
import re

def get_recipe(soup):
    def get_text_if_not_none(class_attrs):
        text = soup.find(attrs={'class': class_attrs})
        if text is not None:
            text = text.get_text()
        return text

    recipe = {}
    recipe['title'] = soup.find('h1').text

    # metadata (times, difficulty, servings)
    metadata = {}

    times_soup = soup.findAll('time')
    for item in times_soup:
        tmp = item.parent.previous_sibling.text[:-1]
        metadata[tmp] = item.text

    metadata['difficulty'] = get_text_if_not_none('masthead__skill-level')
    metadata['servings'] = get_text_if_not_none('masthead__servings')

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


    