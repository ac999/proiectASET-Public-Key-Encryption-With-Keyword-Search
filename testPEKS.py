import unittest

from timeout_decorator import timeout

import peks



FUNC_TIMEOUT = 60
# Change SIGNALS to False if on Windows
SIGNALS = True

class TestPEKS(unittest.TestCase):

    def test_generate_keys(self):
        client = peks.PEKSClient()
        public_key_list = list()
        private_key_list = list()
        for i in range(100):
            client.KeyGen()
            public_key_list.append(client.publ)
            private_key_list.append(client.priv)
        self.assertEqual(len(public_key_list), len(set(public_key_list)),
        msg="Public key duplicates found.")
        for key in public_key_list:
            self.assertNotEqual(key in private_key_list, True,
            msg="Public key found in private key list.")

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
        client.PEKS(word),
        msg="Same PEKS for same word."
        )


    def test_trapdoor_method(self):
        for i in range(10):
            client = peks.PEKSClient()
            client.KeyGen()
            word = "Word2"
            self.assertEqual(
            client.Trapdoor(word),
            client.Trapdoor(word),
            msg="Trapdoors are not equal for same client and word"
            )
            client2 = peks.PEKSClient()
            client2.KeyGen()
            self.assertNotEqual(client.Trapdoor(word),
            client2.Trapdoor(word),
            msg="Trapdoors are equal for same word and different clients.")

    def test_PEKSServer(self):
        client = peks.PEKSClient()
        client.KeyGen()
        word = "Word3"
        server = peks.PEKSServer(client.publ)
        S = client.PEKS(word)
        T_w = client.Trapdoor(word)
        self.assertEqual(server.Test(S, T_w), True, msg="PEKS not working.")

if __name__ == '__main__':
    unittest.main()
