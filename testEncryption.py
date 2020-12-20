import unittest

import fernet

from secrets import randbelow

class TestEncryption(unittest.TestCase):
    def testEncryptionDecryption(self):
        salt = fernet.generateSalt()
        for i in range(10):
            key = randbelow(
            0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
            )
            ctxt = fernet.encrypt("Test Encryption Algorithm", key, salt)
            ptxt = fernet.decrypt(ctxt, key, salt)
            self.assertEqual("Test Encryption Algorithm", ptxt.decode('utf-8'),
            msg="Decrypted text should be \"Test Encryption Algorithm\".")

if __name__ == '__main__':
    unittest.main()
