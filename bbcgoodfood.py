from web_scraper import get_content_from_url
from bs4 import BeautifulSoup
import re
import recipe_repo

# if a url is a category/collection, it gets the headings from those sections and checks again, until it finds a recipe
def process_url(url):
    print("Processing url: {0}".format(url))
    if is_url_category_or_collection(url):
        [process_url(heading_url) for heading_url in get_headings_from_section(url)]
    else:
        process_recipe(url)


# scrapes the recipe data and adds it to the database, if its not already in there
def process_recipe(url):
    if recipe_repo.is_recipe_in_db(url):
        print("Recipe already in DB: {0}".format(url))
        return
    
    soup = get_content_from_url(url)
    recipe = None
    try:
        recipe = get_recipe(soup)
    except:
        print("Skipped recipe with url: {0}".format(url))
    
    if recipe is not None:
        recipe['url'] = url
        recipe_repo.insert_one(recipe)
        print("Added recipe: {0}".format(recipe['title']))


# gets a list of urls from the headings of all pages in a section
def get_headings_from_section(url):
    soup = get_content_from_url(url)
    pages_soup = [soup] + [get_content_from_url(page_url) for page_url in get_pagination_urls(soup)]
    heading_urls = []
    for page_soup in pages_soup:
        heading_urls += get_heading_urls(page_soup)
    return heading_urls


# gets a list of urls from the headings of a page
def get_heading_urls(soup):
    return [title_soup.get('href') for title_soup in soup.findAll('a', attrs={'class': 'standard-card-new__article-title'})]


# gets a list of urls for the other pages in a category/collection that aren't currently selected 
# e.g. if on page 1 of 3, it will get the urls of pages 2 and 3
def get_pagination_urls(soup):
    pagination_items = soup.find('div', attrs={'pagination'})
    if pagination_items is None or len(pagination_items) is 1:
        return []
    pagination_items = pagination_items.findAll('a', attrs={'class': 'pagination-item'})
    return [item.get('href') for item in pagination_items]


# returns true if the url points to a category or a collection, but false if it is a recipe
def is_url_category_or_collection(url):
    return re.search("(?<=recipes\/)(category|collection)", url) is not None
    

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


    