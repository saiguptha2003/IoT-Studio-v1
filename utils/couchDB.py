import couchdb

from constants import DBNAME
couch = couchdb.Server('http://admin:iotstudio@localhost:5984/')
DBNAME='iotstudio'
cdb=couch[DBNAME]
