import pymongo

connection_string = 'mongodb://127.0.0.1:27017'
client = pymongo.MongoClient(connection_string)

database = client['webscraper']
collection = database['recipes']

def find(query):
    return collection.find(query)

def find_one(query):
    return collection.find_one(query)

def insert_one(recipe):
    collection.insert_one(recipe)