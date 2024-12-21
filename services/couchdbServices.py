import json

from flask import jsonify
import couchdb
from constants import DBNAME
from utils import couch
def createDocumentForUser(userId: str,username :str, emailId: str):
    cdb=None
    if DBNAME not in couch:
        print(f"Database '{DBNAME}' not found. Creating it...")
        cdb = couch.create(DBNAME)
    else:
        cdb = couch[DBNAME]
        print(f"Connected to the database: {DBNAME}")
    doc = {'type': 'test', 'message': 'This is a test document.'}
    doc_id, doc_rev = cdb.save(doc)
    print(f"Document saved with ID: {doc_id}, Revision: {doc_rev}")

    doc={
        "_id":userId,
        "username":username,
        "email":emailId
    }
    try:
        cdb.save(doc)
    except couchdb.http.ResourceConflict:
        return jsonify({
            "error":"failed to create user",
            "message":"Could not create couchdb document for user",
            "status_code":230
        })
    userDoc=cdb[userId]
    userDoc['status_code']=200
    return json.dumps(userDoc,indent=4)