import requests
from bs4 import BeautifulSoup

root_url = "https://www.bbcgoodfood.com/"

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
headers = {'User-Agent': user_agent}

def get_content_from_url(url):
    response = requests.get(url, headers=headers, timeout=100)
    return BeautifulSoup(response.content, 'html.parser')


def get_recipe(url):
    content = get_content_from_url(url)

    title = content.find('h1').text

    times = content.findAll('time')

    # metadata (times, difficulty, servings)
    metadata = {}
    for item in times:
        tmp = item.parent.previous_sibling.text[:-1]
        metadata[tmp] = item.text

    metadata['difficulty'] = content.find(attrs={'class': 'masthead__skill-level'}).get_text()
    metadata['servings'] = content.find(attrs={'class': 'masthead__servings'}).get_text()

    recipe = {
        'title': title,
        'metadata': metadata
    }

    print(recipe)

get_recipe('https://www.bbcgoodfood.com/recipes/old-delhi-style-butter-chicken')


# def scrape_categories(url):
