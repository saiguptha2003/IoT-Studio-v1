from secrets import token_bytes, token_hex, token_urlsafe
import uuid


def generateUUID(type):
    switcher={
    'int':uuid.uuid4().int,
    'hex':uuid.uuid4().hex,
    'classic':str(uuid.uuid4())
    }
    return switcher.get(type,None)
    
def generateTokens(type,nbytes):
    switcher={
        'bytes':str(token_bytes(nbytes)),
        'hex':str(token_hex(nbytes)),
        'urlsafe':str(token_urlsafe())
    }
    return switcher.get(type,None)
    