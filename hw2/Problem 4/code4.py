import binascii
from Cryptodome.Cipher import AES
import hmac
import hashlib
from config import *
from Cryptodome.PublicKey import RSA


#raw data
spkc1 = '00ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffe0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001'

#convert to int
spkc1_int = int(spkc1, 16)

#RSA key factorize(ta.cns.com)
c1_p = mason(521)
c1_q = int(spkc1,16) // c1_p
c1 = rsa_key(c1_p, c1_q, 65537)
key = RSA.construct((c1.n, c1.e, c1.d))

#write to server_key.pem
f = open('server_key.pem', 'wb')
f.write(key.export_key(format='PEM'))
f.close()


