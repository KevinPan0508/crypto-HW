import random
import time
from pwn import *
from Cryptodome.Util.number import inverse, getStrongPrime
from Cryptodome.Cipher import AES

alice = remote('cns.csie.org', '30001')
bob = remote('cns.csie.org', '30002')

# Attacker generates own public_key, prime and g
txt = alice.recvuntil(b'g: ')
p = int(txt.decode().replace('g: ', '').replace('p: ','').strip('\n'))
txt = alice.recvuntil(b'public: ')
g = int(txt.decode().replace('public: ', '').strip('\n'))
public_alice = int(alice.recvline().decode().strip('\n'))
my_private = random.randint(2, p - 2)
my_public = pow(g, my_private, p)

# Attacker send own public_key, prime and g
bob.sendline("p: " + str(p))
bob.sendline("g: " + str(g))
bob.sendline("public: " + str(my_public))
txt = bob.readline()
public_bob = int(txt.decode().replace('public: ','').strip('\n'))
iv_hex = bob.readline().decode().replace('iv: ' ,'').strip('\n')


# Attacker sends iv and public to Alice
alice.sendline("public: " + str(my_public))
my_iv = '01010101010101010101010101010101'
alice.sendline("iv: " + my_iv)
txt = alice.recvline().decode().strip('\n')
enc_flaga1 = txt.replace('flag1: ', '')

# Attacker decrypt flaga1 
mask = (1 << 128) - 1
symmetric_key_ma = (pow(public_alice, my_private, p)) & mask
symmetric_key_mb = (pow(public_bob, my_private, p)) & mask
iv = bytes.fromhex(my_iv)
real_iv = bytes.fromhex(iv_hex)
key_ma = symmetric_key_ma.to_bytes(16, 'big')
key_mb = symmetric_key_mb.to_bytes(16, 'big')
decrypter_ma = AES.new(key=key_ma, mode=AES.MODE_CBC, iv=iv)
encrypter_ma = AES.new(key=key_ma, mode=AES.MODE_CBC, iv=iv)
decrypter_mb = AES.new(key=key_mb, mode=AES.MODE_CBC, iv=real_iv)
encrypter_mb = AES.new(key=key_mb, mode=AES.MODE_CBC, iv=real_iv)
flaga1 = decrypter_ma.decrypt(bytes.fromhex(enc_flaga1))
e_mb_flaga1 = (encrypter_mb.encrypt(flaga1)).hex()

# Attacker sends E(g^bm, flaga1) to Bob
bob.sendline('flag1: ' + e_mb_flaga1)
txt = bob.recvline().decode().strip('\n')
enc_flagb1 = txt.replace('flag1: ', '')
flagb1 = decrypter_mb.decrypt(bytes.fromhex(enc_flagb1))
e_ma_flagb1 = (encrypter_ma.encrypt(flagb1)).hex()


#Bob sends E(Symmetric_key, FLAG'''B1) to Alice

alice.sendline('flag1: ' + e_ma_flagb1)
txt = alice.recvline().decode().strip('\n')
enc_flaga2 = txt.replace('flag2: ', '')
flaga2 = decrypter_ma.decrypt(bytes.fromhex(enc_flaga2))

print(flaga1.decode() + flagb1.decode() + flaga2.decode())








