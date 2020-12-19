import unittest

from timeout_decorator import timeout

import fernet

import peks



FUNC_TIMEOUT = 60
# Change SIGNALS to False if on Windows
SIGNALS = True

class TestPEKS(unittest.TestCase):

    def test_generate_keys(self):
        client = peks.PEKSClient()
        client.KeyGen()
        client.dumpKeys()
        with open("key.priv", "r", encoding="utf-8") as f:
            assert client.priv == int(f.read())
        with open("key.pub", "r", encoding="utf-8") as f:
            assert client.publ == int(f.read())
        salt = fernet.generateSalt()
        ctxt = fernet.encrypt("Test Encryption Algorithm", client.publ, salt)
        ptxt = fernet.decrypt(ctxt, client.publ, salt)
        assert "Test Encryption Algorithm"==ptxt.decode('utf-8')

    def test_peks_method(self):
        client = peks.PEKSClient()
        client.KeyGen()
        word = "Word1"
        print(client.PEKS(client.publ, client.h, word))

if __name__ == '__main__':
    unittest.main()
