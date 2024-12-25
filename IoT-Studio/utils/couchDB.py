import json
import os
import couchdb
COUCHDB_URL=os.getenv('COUCHDB_URL')
DATABASE_NAME=os.getenv('DATABASE_NAME')
couch = couchdb.Server(COUCHDB_URL)
cdb=couch[DATABASE_NAME]
