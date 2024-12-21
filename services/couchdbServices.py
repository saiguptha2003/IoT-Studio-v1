import json

from flask import jsonify
import couchdb

from constants import DBNAME
def createDocumentForUser(userId: str,username :str, emailId: str):
    couch=couchdb.connect("https://admin:iotstudio@couchdb-xfm8.onrender.com/")
    if DBNAME not in couch:
        cdb = couch.create(DBNAME)
    else:
        cdb = couch[DBNAME]
    
    doc={
        "_id":userId,
        "username":username,
        "email":emailId
    }
    try:
        cdb = couch[DBNAME]
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