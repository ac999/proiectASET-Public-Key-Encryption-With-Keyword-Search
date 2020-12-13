import hashlib
import json
import requests
import logger

def hash(plaintext):
    _salt = "pkekspkekspkekspkekspkekspkekspkekspkeks00000000000000000000000000"
    hr = hashlib.scrypt(plaintext.encode("utf-8"), salt = _salt.encode('utf-8'),
    n = 16384, r = 8, p = 1)
    return hr.hex()

def hibp_password(password):
    try:
        hash = hashlib.sha1(password.encode())
        hash = hash.hexdigest().upper()

        response = requests.get("https://api.pwnedpasswords.com/range/{}"\
        .format(hash[:5]))

        if (hash[5:] in list(map(lambda x: x.decode('utf-8').split(':')[0],
        response.content.splitlines()))):
            return (True, False)

        return (True, True)

    except Exception as e:
        print(e)
        return (False, True)

def dump_json(PATH, jsonobject):

    try:
        with open(PATH, 'w') as fp:
            json.dump(jsonobject, fp, indent = 4)

    except Exception as e:
        raise e

def load_json(PATH):
    try:
        with open(PATH) as fp:
            return json.load(fp)

    except Exception as e:
        print(e)
        raise e

def create_json(**kwargs):
    return json.dumps(kwargs)

def validate_user(jsonobject):
    fields = ["usr", "pwd"]
    data = json.loads(jsonobject)
    if set(data.keys()) != set(fields):
        return False
    return True
