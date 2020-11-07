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

def count():
    return collection.count_documents({})

def count_query(query):
    return collection.count_documents(query)

def insert_if_not_in_db(recipe):
    if find_one({'url': recipe['url']}) is None:
        insert_one(recipe)
        return True
    return False