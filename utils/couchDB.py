import json
import couchdb
from constants import DBNAME

couch = couchdb.Server('http://admin:iotstudio@couchdb:5984/')

cdb=couch[DBNAME]
# json_file_path=""
# with open(json_file_path, 'a') as file:
#     cdb = json.load(file)