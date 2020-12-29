import unittest

from timeout_decorator import timeout

import curve25519

FUNC_TIMEOUT = 60
# Change SIGNALS to False if on Windows
SIGNALS = True

class TestX25519(unittest.TestCase):

    def test_swap(self):
        a = 5000
        b = 10000
        # a shoud be swapped with b:
        a,b = curve25519.swap25519(a, b, 1)
        self.assertEqual(a, 10000, "a should've been 10000")
        self.assertEqual(b, 5000, "b should've been 5000")
        # a and b should remain the same:
        a = 5000
        b = 10000
        a,b = curve25519.swap25519(a, b, 0)
        self.assertEqual(b, 10000, "b should've been 10000")
        self.assertEqual(a, 5000, "a should've been 5000")

    def test_init(self):

        _curve = curve25519.Curve()
        self.assertEqual(_curve.name, "x25519", "Curve name should be 'x25519'")

    @timeout(FUNC_TIMEOUT, use_signals=SIGNALS)
    def test_generate_keys(self):

        _curve = curve25519.Curve()
        private_key, public_key = _curve.generateKeypair()
        self.assertNotEqual(public_key, None, "Public key should not be empty")
        self.assertNotEqual(private_key, None, "Private key should not be empty")
        private_key2, public_key2 = _curve.generateKeypair()
        self.assertNotEqual(public_key, public_key2, "Generated public keys must\
        differ.")
        self.assertNotEqual(private_key, private_key2, "Generated private keys\
        must differ.")

    def test_x25519(self):
        _curve = curve25519.Curve()
        private_key_Alice, public_key_Alice = _curve.generateKeypair()
        private_key_Bob, public_key_Bob = _curve.generateKeypair()
        s1 = _curve.x25519(private_key_Alice, public_key_Bob)
        s2 = _curve.x25519(private_key_Bob, public_key_Alice)
        self.assertEqual(s1, s2, "Shared secret is not equal to both parts.")
if __name__ == '__main__':
    unittest.main()
