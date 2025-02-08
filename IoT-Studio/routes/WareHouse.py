import base64
from datetime import datetime, timezone
import io
import json
import logging
import uuid
from flask import Blueprint, jsonify, request, send_file
from services import generateUUID,generateTokens
from utils import token_required, cdb,getUniqueIDInt
from cache import redisClient
WareHouseBP = Blueprint("WareHouseBP", __name__)


@WareHouseBP.route('/getConnectFilesList', methods=['GET'])
@token_required
def getConnectFiles(userid, email, username):
    try:
        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc or "_rev" not in userDoc:
            userDoc = cdb.get(userid)
        if not userDoc:
            return jsonify({"error": "User not found"}), 404
        connect_files = userDoc.get("ConnectFiles", [])
        return jsonify({"connect_files": connect_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@WareHouseBP.route('/getConnectFile/<fileId>', methods=['GET'])
@token_required
def getConnectFileById(userid, email, username, fileId):
    try:
        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc or "_rev" not in userDoc:
            userDoc = cdb.get(userid)  
        
        if not userDoc:
            return jsonify({"error": "User not found"}), 404
        connect_files = userDoc.get("ConnectFiles", [])
        file_entry = next((f for f in connect_files if f["uuid"] == fileId), None)
        if not file_entry:
            return jsonify({"error": "File not found in user records"}), 404

        filename = file_entry["filename"]
        ConnectFilesDOCID = "555826f494c24297671d768db101685a"  
        fileDoc = cdb.get(ConnectFilesDOCID)
        if not fileDoc or "_attachments" not in fileDoc or fileId not in fileDoc["_attachments"]:
            return jsonify({"error": "File not found in storage"}), 404
        logging.info(fileDoc)
        file_content = cdb.get_attachment(ConnectFilesDOCID, fileId)
        if not file_content:
            return jsonify({"error": "Error retrieving file"}), 500
        content_type = fileDoc["_attachments"][fileId]["content_type"]
        return send_file(
            io.BytesIO(file_content.read()),
            as_attachment=True,
            download_name=f"{filename}.xlsx",
            mimetype=content_type
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500