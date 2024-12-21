import couchdb

from constants import DBNAME
couch = couchdb.Server('https://admin:iotstudio@couchdb-xfm8.onrender.com/')
DBNAME='iotstudio'
cdb=couch[DBNAME]
