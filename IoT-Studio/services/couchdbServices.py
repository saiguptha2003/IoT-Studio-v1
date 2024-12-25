import json
from flask import jsonify
import couchdb
from utils import cdb
def createDocumentForUser(userId: str,username :str, emailId: str,created_at):
    doc={
        "_id":userId,
        "username":username,
        "email":emailId,
        "created_at":created_at
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