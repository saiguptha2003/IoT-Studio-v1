import uuid


def generateUUID(type):
    switcher={
    'int':uuid.uuid4().int,
    'hex':uuid.uuid4().hex,
    'classic':str(uuid.uuid4())
    }
    return switcher.get(type,None)
    