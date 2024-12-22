from datetime import datetime
import uuid
from flask import Blueprint, jsonify, request
from utils import token_required
from utils import getUniqueID, cdb

IoTConnectBP = Blueprint("IoTConnect", __name__)

@IoTConnectBP.route("/createServiceConnect", methods=["POST"])
@token_required
def createServicesConnect(userid, email, username):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request, no data provided"}), 400

        data['service_id'] = str(uuid.uuid4())  # Convert UUID to string
        data['created_at'] = str(int(datetime.now().timestamp()))  # Use timestamp instead of datetime
        # data['userId']=userid
        # data['username'] = username
        # data['email']=email
        user_doc = cdb.get(userid)
        
        if not user_doc:
            return jsonify({"error": "User document not found"}), 404
        
        if 'IoTConnect' not in user_doc:
            user_doc['IoTConnect'] = []
        
        user_doc['IoTConnect'].append(data)
        cdb.save(user_doc)

        return jsonify({
            "message": "Service connection created successfully.",
            "service_id": data['service_id'],
            "IoTConnect": user_doc['IoTConnect']
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
