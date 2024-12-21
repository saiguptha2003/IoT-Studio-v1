import couchdb
from constants import DBNAME

couch = couchdb.Server('https://admin:iotstudio@couchdb-xfm8.onrender.com/')
# cdb=couch[DBNAME]
import json
from couchdb.http import ResponseBody

# Patch the decode method for ResponseBody if not already present
if not hasattr(ResponseBody, 'decode'):
    def decode(self):
        return json.loads(self.read().decode('utf-8'))
    setattr(ResponseBody, 'decode', decode)
