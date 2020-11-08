import bbcgoodfood

# starts the scraper to add recipes to the database
def start():
    bbcgoodfood.process_url('https://www.bbcgoodfood.com/recipes/category')


# starts the scraper to add tags to each recipe in the database
def start_tag_search():
    bbcgoodfood.process_url_for_tags('https://www.bbcgoodfood.com/recipes/category')
