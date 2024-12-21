import couchdb
from constants import DBNAME
couch = couchdb.Server('https://admin:iotstudio@couchdb-xfm8.onrender.com/')

if DBNAME not in couch:
    print(f"Database '{DBNAME}' not found. Creating it...")
    cdb = couch.create(DBNAME)
else:
    cdb = couch[DBNAME]
    print(f"Connected to the database: {DBNAME}")
doc = {'type': 'test', 'message': 'This is a test document.'}
doc_id, doc_rev = cdb.save(doc)
print(f"Document saved with ID: {doc_id}, Revision: {doc_rev}")
