from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
import json

cluster = Cluster('couchbase://localhost')
with open('credentials.json') as json_file:
    data = json.load(json_file)
authenticator = PasswordAuthenticator(data['username'], data['password'])
cluster.authenticate(authenticator)

cb = cluster.open_bucket('Recipes')

def create_key(title):
    return title.lower().replace(' ', '_')


def insert_recipe(key, recipe_json):
    try:
        cb.insert(key, recipe_json)
    except:
        print("Key already exists")


def upsert_recipe(key, recipe_json):
    try:
        cb.upsert(key, recipe_json)
    except:
        print("Upsert error")


def get_recipe(key):
    try:
        return cb.get(key).value
    except:
        return None

# print(cb.get('Lamb_vindaloo').value)