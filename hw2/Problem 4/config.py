from gmpy2 import *
from scapy.layers.tls.crypto.prf import PRF
from scapy.layers.tls.crypto.hash import _tls_hash_algs
from scapy.layers.tls.crypto.h_mac import _tls_hmac_algs
from scapy.compat import bytes_encode

class rsa_key:
    def __init__(self, p, q, e):
        self.e = e
        self.p = p
        self.q = q
        self.n = self.p *self.q
        self.phi = int(str(mpz(self.p-1) * mpz(self.q-1)))
        self.d = int(str(invert(mpz(self.e), self.phi)))

def mason(n):
    return (2**n)-1

def encrypt(m, key):
    return pow(m, key.e, key.n)

def decrypt(c, key):
    return pow(c, key.d, key.n)


def tls12_SHAPRF(secret, label, seed, req_len):
    return tls_P_SHA1(secret, label + seed, req_len)

def tls_P_SHA1(secret, seed, req_len):
    return tls_P_hash(secret, seed, req_len, _tls_hmac_algs["HMAC-SHA"])

def tls_P_hash(secret, seed, req_len, hm):
    hash_len = hm.hash_alg.hash_len
    n = (req_len + hash_len - 1) // hash_len
    seed = bytes_encode(seed)

    res = b""
    a = hm(secret).digest(seed)  # A(1)

    while n > 0:
        res += hm(secret).digest(a + seed)
        a = hm(secret).digest(a)
        n -= 1

    return res[:req_len]

def compute_master_secret(pre_master_secret, client_random, server_random):
    seed = client_random + server_random
    label = b'master secret'
    return tls12_SHAPRF(pre_master_secret, label, seed, 48)


def derive_key_block(master_secret, server_random, client_random, req_len):
    seed = server_random + client_random
    return tls12_SHAPRF(master_secret, b"key expansion", seed, req_len)