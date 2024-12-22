from datetime import time
import uuid
from flask import Blueprint, jsonify,request

from utils import token_required
from utils import getUniqueID,cdb

IoTConnectBP=Blueprint("IoTConnect",__name__)


@IoTConnectBP.route("/createServiceConnect", methods=["Post"])
@token_required
def createServicesConnect():
    try:
        userid = request.args.get('userid')
        email = request.args.get('email')
        username = request.args.get('username')
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid request, no data provided"}), 400

        data['service_id'] = uuid.uuid4()
        data['created_at'] = str(int(time.time()))
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
