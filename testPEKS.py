import unittest

from timeout_decorator import timeout

import peks



FUNC_TIMEOUT = 60
# Change SIGNALS to False if on Windows
SIGNALS = True

class TestPEKS(unittest.TestCase):

    def test_generate_keys(self):
        client = peks.PEKSClient()
        for i in range(100):
            client.KeyGen()
            self.assertNotEqual(client.priv, client.publ,msg="Keys should differ")

        client.dumpKeys()
        with open("key.priv", "r", encoding="utf-8") as f:
            self.assertEqual(client.priv, int(f.read()))
        with open("key.pub", "r", encoding="utf-8") as f:
            self.assertEqual(client.publ, int(f.read()))

    def test_peks_method(self):
        client = peks.PEKSClient()
        client.KeyGen()
        word = "Word1"
        self.assertNotEqual(
        client.PEKS(word),
        client.PEKS(word)
        )


    def test_trapdoor_method(self):
        for i in range(10):
            client = peks.PEKSClient()
            client.KeyGen()
            word = "Word1"
            self.assertEqual(
            client.Trapdoor(word),
            client.Trapdoor(word)
            )
            client2 = peks.PEKSClient()
            client2.KeyGen()
            self.assertNotEqual(client.Trapdoor(word),
            client2.Trapdoor(word))

    def test_PEKSServer(self):
        client = peks.PEKSClient()
        client.KeyGen()
        word = "Word1"
        server = peks.PEKSServer(client.publ)
        S = client.PEKS(word)
        T_w = client.Trapdoor(word)
        self.assertEqual(server.Test(S, T_w), True, msg="PEKS not working.")

if __name__ == '__main__':
    unittest.main()
