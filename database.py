from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
import json

cluster = Cluster('couchbase://localhost')
with open('credentials.json') as json_file:
    data = json.load(json_file)
authenticator = PasswordAuthenticator(data['username'], data['password'])
cluster.authenticate(authenticator)

cb = cluster.open_bucket('Recipes')


def insert_recipe(recipe_json):
    key = recipe_json['title'].lower().replace(' ', '_')
    cb.insert(key, recipe_json)


# print(cb.get('Lamb_vindaloo').value)