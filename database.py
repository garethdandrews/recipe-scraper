from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
import json

cluster = Cluster('couchbase://localhost')

with open('credentials.json') as json_file:
    data = json.load(json_file)
authenticator = PasswordAuthenticator(data['username'], data['password'])