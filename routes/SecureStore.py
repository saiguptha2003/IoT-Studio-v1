from datetime import datetime, timezone
from flask import Blueprint, jsonify, request
from services import generateUUID
from utils import token_required, cdb,getUniqueIDInt
SecureStoreBP = Blueprint("SecureStoreBP", __name__)

@SecureStoreBP.route('/createSecureId', methods=['POST'])
@token_required
def createUniqueID(userid, email, username):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request, no data provided"}), 400

        type_of_id = data.get('type_of_id')
        description = data.get('description')
        secureid_name = data.get('secureid_name')

        if not type_of_id:
            return jsonify({"error": "Missing required field: 'type_of_id'"}), 400
        if not description:
            return jsonify({"error": "Missing required field: 'description'"}), 400
        if not secureid_name:
            return jsonify({"error": "Missing required field: 'secureid_name'"}), 400

        userDoc = cdb.get(userid)
        if not userDoc:
            return jsonify({"error": "User document not found"}), 404

        if 'SecureStore' not in userDoc:
            userDoc['SecureStore'] = []
        if not any('SecureID' in entry for entry in userDoc['SecureStore']):
            userDoc['SecureStore'].append({'SecureID': []})

        for secureEntry in userDoc['SecureStore']:
            if 'SecureID' in secureEntry:
                for existingEntry in secureEntry['SecureID']:
                    if existingEntry.get('secureid_name') == secureid_name:
                        return jsonify({"error": f"secureid_name '{secureid_name}' already exists."}), 400

        secure_id = generateUUID(type_of_id)
        unique_id = getUniqueIDInt()
        created_at = str(datetime.now(timezone.utc).timestamp())

        new_entry = {
            "id": str(unique_id),
            "secure_id": str(secure_id),
            "secureid_name": secureid_name,
            "type_of_id": type_of_id,
            "description": description,
            "created_at": created_at
        }
        for secureEntry in userDoc['SecureStore']:
            if 'SecureID' in secureEntry:
                secureEntry['SecureID'].append(new_entry)
        cdb.save(userDoc)
        return jsonify({
            "message": "Secure ID created successfully.",
            "secure_id": secure_id,
            "entry": new_entry
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@SecureStoreBP.route('/deleteSecureID/<id>', methods=['DELETE'])
@token_required
def deleteSecureID(userid, email, username, id):
    try:
        id=str(id)
        if not id:
            return jsonify({"error": "Missing required parameter: 'id'"}), 400

        userDoc = cdb.get(userid)
        if not userDoc or 'SecureStore' not in userDoc:
            return jsonify({"error": "No SecureStore data found for the user."}), 404

        deletedId = None
        for secureEntry in userDoc['SecureStore']:
            if 'SecureID' in secureEntry:
                for entry in secureEntry['SecureID'][:]: 
                    if entry.get('id') == id:
                        secureEntry['SecureID'].remove(entry)
                        deletedId = id
                        break

        if not deletedId:
            return jsonify({"error": f"No Secure ID found with id '{id}'."}), 404

        cdb.save(userDoc)

        return jsonify({
            "message": f"Secure ID with id '{id}' deleted successfully.",
            "deleted_id": deletedId
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@SecureStoreBP.route('/getSecureID/<id>', methods=['GET'])
@token_required
def getSecureID(userid, email, username, id):
    try:
        if not id:
            return jsonify({"error": "Missing required parameter: 'id'"}), 400

        userDoc = cdb.get(userid)
        if not userDoc or 'SecureStore' not in userDoc:
            return jsonify({"error": "No SecureStore data found for the user."}), 404

        for secureEntry in userDoc['SecureStore']:
            if 'SecureID' in secureEntry:
                for entry in secureEntry['SecureID']:
                    if entry.get('id') == id:
                        return jsonify(entry), 200

        return jsonify({"error": f"No Secure ID found with id '{id}'."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
@SecureStoreBP.route('/getAllSecureIDs', methods=['GET'])
@token_required
def getAllSecureIDs(userid, email, username):
    try:
        userDoc = cdb.get(userid)
        if not userDoc or 'SecureStore' not in userDoc:
            return jsonify({"error": "No SecureStore data found for the user."}), 404

        allSecureIds = []
        for secureEntry in userDoc['SecureStore']:
            if 'SecureID' in secureEntry:
                for entry in secureEntry['SecureID']:
                    allSecureIds.append(entry)

        return jsonify(allSecureIds), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
