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
from werkzeug.utils import secure_filename

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
    

@WareHouseBP.route('/deleteConnectFile/<fileId>', methods=['DELETE'])
@token_required
def deleteConnectFileById(userid, email, username, fileId):
    try:
        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc:
            userDoc = cdb.get(userid)
        if not userDoc:
            return jsonify({"error": "User not found"}), 404

        connect_files = userDoc.get("ConnectFiles", [])
        file_entry = next((f for f in connect_files if f["uuid"] == fileId), None)
        if not file_entry:
            return jsonify({"error": "File not found in user records"}), 404
        userDoc["ConnectFiles"] = [f for f in connect_files if f["uuid"] != fileId]
        userDoc["_rev"] = cdb.get(userid)["_rev"]
        cdb.save(userDoc)
        ConnectFilesDOCID = "555826f494c24297671d768db101685a"
        fileDoc = cdb.get(ConnectFilesDOCID)
        if not fileDoc or "_attachments" not in fileDoc or fileId not in fileDoc["_attachments"]:
            return jsonify({"error": "File not found in storage"}), 404
        del fileDoc["_attachments"][fileId]
        fileDoc["_rev"] = cdb.get(ConnectFilesDOCID)["_rev"]
        cdb.save(fileDoc)
        redisClient.set(userid,json.dumps(userDoc))
        return jsonify({"message": "File deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    
@WareHouseBP.route('/getTriggerFilesList', methods=['GET'])
@token_required
def getTriggerFiles(userid, email, username):
    try:
        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc or "_rev" not in userDoc:
            userDoc = cdb.get(userid)
        if not userDoc:
            return jsonify({"error": "User not found"}), 404
        connect_files = userDoc.get("triggers", [])
        return jsonify({"trigger_files": connect_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@WareHouseBP.route('/getTriggerFile/<triggerId>', methods=['GET'])
@token_required
def getTriggerFileById(userid, email, username, triggerId):
    try:
        TRIGGER_DOC_ID = "496f084796a84d1c542e50d439002052"  
        triggerDoc = cdb.get(TRIGGER_DOC_ID)

        if not triggerDoc or triggerId not in triggerDoc:
            return jsonify({"error": "Trigger ID not found"}), 404
        trigger = triggerDoc[triggerId] 
        filepath=trigger['file_path'] 
        FILES_DOC_ID = "c08667781a0bd38fcaeeacc6eb003b3b"
        fileDoc = cdb.get(FILES_DOC_ID)

        if not fileDoc or "_attachments" not in fileDoc or filepath not in fileDoc["_attachments"]:
            return jsonify({"error": "File not found in storage"}), 404
        file_content = cdb.get_attachment(FILES_DOC_ID, filepath)
        if not file_content:
            return jsonify({"error": "Error retrieving file"}), 500
        content_type = fileDoc["_attachments"][filepath]["content_type"]
        logging.info(f"Retrieved file {filepath} from document {FILES_DOC_ID}")

        return send_file(
            io.BytesIO(file_content.read()),
            as_attachment=True,
            download_name=filepath,  
            mimetype=content_type
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@WareHouseBP.route('/deleteTrigger/<triggerId>', methods=['DELETE'])
@token_required
def deleteTriggerById(userid, email, username, triggerId):
    try:
        TRIGGER_DOC_ID = "496f084796a84d1c542e50d439002052"
        FILES_DOC_ID = "c08667781a0bd38fcaeeacc6eb003b3b"
        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc:
            userDoc = cdb.get(userid)
        if not userDoc:
            return jsonify({"error": "User not found"}), 404
        if "triggers" in userDoc:
            userDoc["triggers"] = [t for t in userDoc["triggers"] if t != triggerId]
        userDoc["_rev"] = cdb.get(userid)["_rev"]
        cdb.save(userDoc)
        triggerDoc = cdb.get(TRIGGER_DOC_ID)
        if not triggerDoc or triggerId not in triggerDoc:
            return jsonify({"error": "Trigger ID not found"}), 404

        trigger = triggerDoc.pop(triggerId) 
        filepath = trigger.get('file_path')
        triggerDoc["_rev"] = cdb.get(TRIGGER_DOC_ID)["_rev"]
        cdb.save(triggerDoc)

        if filepath:
            fileDoc = cdb.get(FILES_DOC_ID)
            if fileDoc and "_attachments" in fileDoc and filepath in fileDoc["_attachments"]:
                del fileDoc["_attachments"][filepath]  
                fileDoc["_rev"] = cdb.get(FILES_DOC_ID)["_rev"]
                cdb.save(fileDoc)
        redisClient.set(userid,json.dumps(userDoc))
        return jsonify({"message": "Trigger, user reference, and associated file deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@WareHouseBP.route('/getStaticFileList', methods=['GET'])
@token_required
def getStaticFiles(userid, email, username):
    try:
        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc or "_rev" not in userDoc:
            userDoc = cdb.get(userid)
        if not userDoc:
            return jsonify({"error": "User not found"}), 404
        connect_files = userDoc.get("StaticFiles", [])
        return jsonify({"trigger_files": connect_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@WareHouseBP.route("/staticFile/upload", methods=["POST"])
@token_required
def uploadExcelFile(userid, email, username):
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400

        if not file.filename.endswith(('.xls', '.xlsx','.pdf','.pkl','.docs','.txt','.sh','.bat')):
            return jsonify({"error": "Invalid file format. Only .xls,.xlsx.pdf,.pkl,.docs,.txt,.sh,.bat allowed"}), 400

        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc:
            userDoc = cdb.get(userid)
        if not userDoc:
            return jsonify({"error": "User not found"}), 404

        file_uuid = str(uuid.uuid4())

        StaticFileDOCID = "71cfbf7ba7687d23841cbb0dca00063f"  
        fileDoc = cdb.get(StaticFileDOCID)
        if not fileDoc:
            return jsonify({"error": "File storage document not found"}), 404
        fileDoc["_rev"] = fileDoc["_rev"]
        filename = secure_filename(file.filename)
        file_content = base64.b64encode(file.read()).decode("utf-8")

        fileDoc["_attachments"] = fileDoc.get("_attachments", {})
        fileDoc["_attachments"][file_uuid] = {
            "content_type": file.content_type,
            "data": file_content
        }
        cdb.save(fileDoc)
        if "StaticFiles" not in userDoc:
            logging.info("in the var")
            userDoc["StaticFiles"] = []
        userDoc["StaticFiles"].append({"uuid": file_uuid, "filename": filename, "timeStamp":datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
        userDoc["_rev"] = cdb.get(userid)["_rev"]
        cdb.save(userDoc)
        redisClient.set(userid,json.dumps(userDoc))
        return jsonify({"message": "File uploaded successfully", "file_uuid": file_uuid, "filename": filename}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


@WareHouseBP.route('/staticFile/delete/<staticFileId>', methods=['DELETE'])
@token_required
def getStaticDelete(userid, email, username,staticFileId):
    try:
        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc:
            userDoc = cdb.get(userid)
        if not userDoc:
            return jsonify({"error": "User not found"}), 404
        StaticFileDOCID = "71cfbf7ba7687d23841cbb0dca00063f"  
        fileDoc = cdb.get(StaticFileDOCID)
        if not fileDoc or "_attachments" not in fileDoc:
            return jsonify({"error": "File storage document not found"}), 404
        if staticFileId not in fileDoc["_attachments"]:
            return jsonify({"error": "File not found in storage"}), 404
        del fileDoc["_attachments"][staticFileId]
        cdb.save(fileDoc)
        if "StaticFiles" in userDoc and isinstance(userDoc["StaticFiles"], list):
            userDoc["StaticFiles"] = [f for f in userDoc["StaticFiles"] if f["uuid"] != staticFileId]
        userDoc["_rev"] = cdb.get(userid)["_rev"]
        cdb.save(userDoc)
        redisClient.set(userid,json.dumps(userDoc))
        return jsonify({"message": "File Deleted successfully", "file_uuid": staticFileId}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@WareHouseBP.route('/staticFiles/delete', methods=['DELETE'])
@token_required
def deleteMultipleStaticFiles(userid, email, username):
    try:
        data = request.get_json()
        if not data or "fileIds" not in data:
            return jsonify({"error": "Missing fileIds in request"}), 400

        fileIds = data["fileIds"]
        if not isinstance(fileIds, list) or not fileIds:
            return jsonify({"error": "fileIds must be a non-empty list"}), 400
        userDoc = json.loads(redisClient.get(userid) or '{}')
        if not userDoc or "_rev" not in userDoc:
            userDoc = cdb.get(userid)  
        if not userDoc:
            return jsonify({"error": "User not found"}), 404
        StaticFileDOCID = "71cfbf7ba7687d23841cbb0dca00063f"
        fileDoc = cdb.get(StaticFileDOCID)
        if not fileDoc or "_attachments" not in fileDoc:
            return jsonify({"error": "File storage document not found"}), 404

        deleted_files = []
        for fileId in fileIds:
            if fileId in fileDoc["_attachments"]:
                del fileDoc["_attachments"][fileId]
                deleted_files.append(fileId)
        if not deleted_files:
            return jsonify({"error": "No valid files found to delete"}), 404
        fileDoc["_rev"] = cdb.get(StaticFileDOCID)["_rev"]
        cdb.save(fileDoc)
        if "StaticFiles" in userDoc and isinstance(userDoc["StaticFiles"], list):
            userDoc["StaticFiles"] = [f for f in userDoc["StaticFiles"] if f["uuid"] not in deleted_files]
        userDoc["_rev"] = cdb.get(userid)["_rev"]
        cdb.save(userDoc)
        redisClient.set(userid, json.dumps(userDoc))
        return jsonify({"message": "Files deleted successfully", "deleted_files": deleted_files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

