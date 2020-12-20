from aspects import log_errors

from timeout_decorator import timeout

from utils import hash, hash2, int_to_bytes
import curve25519
from fernet import encrypt
# set timeout in seconds for timeout_decorator
TIMEOUT = 30
# set SIGNALS to False if on Windows
SIGNALS = True
# Construction using bilinear maps
class PEKSClient:
    @log_errors
    def __init__(self):
        self._curve = curve25519.Curve()
        self.priv = None
        self.publ = None
        self.h = None
        self.H1 = hash
        self.H2 = hash2

    # Save keys to file
    def dumpKeys(self):
        with open("key.priv", 'w+', encoding='utf-8') as f:
            f.write("{}".format(self.priv))
        with open("key.pub", "w+", encoding='utf-8') as f:
            f.write("{}".format(self.publ))

    # Load keys to file
    def loadKeys(self):
        with open("key.priv", 'r', encoding='utf-8') as f:
            self.priv = int(f.read())
        with open("key.pub", 'r', encoding='utf-8') as f:
            self.publ = int(f.read())
        self.h = _curve.x25519(self.publ, self.priv)

    # Generates a public/private key pair (private, public)
    @timeout(TIMEOUT, use_signals=SIGNALS)
    @log_errors
    def KeyGen(self):
        priv, publ =  self._curve.generateKeypair()
        self.priv = priv
        self.publ = publ
        self.h = self._curve.x25519(self.publ, self.priv)

    # For a public key A_pub and a word W, produces a searchable encryption of W
    @log_errors
    def PEKS(self, W):
        r = self._curve.randomElement()
        t = encrypt(self.H1(W), self._curve.x25519(self.h, r)).decode('utf8')
        output = (self._curve.x25519(self.publ,r), self.H2(t))
        return output

    # Output T_w = H1(w)**alpha
    @log_errors
    def Trapdoor(self, W):
        T_w = self._curve.x25519(int(self.H1(W),16), self.priv)
        return T_w

class PEKSServer:
    @log_errors
    def __init__(self, key):
        '''Client's public key'''
        self.key = key
        self.H2 = hash2

    @log_errors
    def Test(self, S, T_w):
        A, B = S
        A = int_to_bytes(A)
        T_w = int_to_bytes(T_w)
        return self.H2(encrypt(T_w, A)) == B
