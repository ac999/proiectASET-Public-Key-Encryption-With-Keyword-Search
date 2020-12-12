import hashlib
import json

def hash(plaintext):
    _salt = "pkekspkekspkekspkekspkekspkekspkekspkeks00000000000000000000000000"
    hr = hashlib.scrypt(plaintext.encode("utf-8"), salt = _salt.encode("utf-8"),
    n = 16384, r = 8, p = 1)
    return hr.hex()

def dump_json(PATH, DICTIONARY):
    try:
        with open(PATH, 'w') as fp:
            json.dump(DICTIONARY, indent = 4)

    except Exception as e:
        raise e

def load_json(PATH):
    try:
        with open(PATH) as fp:
            return json.load(fp)

    except Exception as e:
        print(e)
        raise e
