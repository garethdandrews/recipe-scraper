import pymongo

connection_string = 'mongodb://172.17.0.2:27017'
client = pymongo.MongoClient(connection_string)

database = client['webscraper']
collection = database['recipes']

def find(query):
    return collection.find(query)

def find_one(query):
    return collection.find_one(query)

def insert_one(recipe):
    collection.insert_one(recipe)

def update_one(query, values):
    collection.update_one(query, values)

def count():
    return collection.count_documents({})

def count_query(query):
    return collection.count_documents(query)

def find_recipe_by_url(url):
    return find_one({'url': url})

def insert_if_not_in_db(recipe):
    if find_recipe_by_url(recipe['url']) is None:
        insert_one(recipe)
        return True
    return False

def is_recipe_in_db(url):
    if find_recipe_by_url(url):
        return True
    return False

def add_tag_to_recipe(url, tag):
    query = {'url': url}
    values = {'$push': {'tags': tag}}
    update_one(query, values)