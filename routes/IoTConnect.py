from flask import Blueprint, jsonify,request

from utils import token_required

IoTConnectBP=Blueprint("IoTConnect",__name__)


@IoTConnectBP.route("/createProject", methods=["Post"])
@token_required
def createProject():
    pass
    
    