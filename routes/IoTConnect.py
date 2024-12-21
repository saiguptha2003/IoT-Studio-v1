from flask import Blueprint, jsonify,request

from utils import token_required
from utils import getUniqueID

IoTConnectBP=Blueprint("IoTConnect",__name__)


@IoTConnectBP.route("/createProject", methods=["Post"])
@token_required
def createProject(userid,email,username):
    data = request.json
    projectName=data.get('project_name', None)
    projectDiscription=data.get('project_discription',None)
    projectCreatedAt=data.get('created at')
    servicesSelected=data.get('services_selected',None)
    userId=data.get('user_id',None)