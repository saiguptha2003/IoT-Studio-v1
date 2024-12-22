import uuid
from werkzeug.security import generate_password_hash, check_password_hash
def hashPassword(password):
    return generate_password_hash(password)
def checkPassword(password,password_hash):
    return check_password_hash(password_hash, password)
def getUniqueID():
    return uuid.uuid4().hex
def getUniqueIDInt():
    return uuid.uuid4().int