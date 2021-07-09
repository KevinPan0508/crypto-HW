import socks
import socket                    
from urllib.parse import urlparse       
from pwn import *     
import hashlib
import binascii
import base64

# Public Key Hash
f = open('./pubkey', 'rb') 
raw = f.readline()
pubkey_byte = raw[32:64]
sha3 = hashlib.sha3_256()
hash_byte = b'.onion checksum' + pubkey_byte + b'\x03'
sha3.update(hash_byte)
checksum = sha3.digest()[:2]
version = b'\x03'
hostname = 'http://' + base64.b32encode(pubkey_byte + checksum + version).decode().lower() + '.onion'                                                                             

#Connect to Server
SOCKS_HOST = 'localhost'                                             
SOCKS_PORT = 9051                                                    
SOCKS_TYPE = socks.PROXY_TYPE_SOCKS5                              
parsed = urlparse(hostname)
socket = socks.socksocket()                                          
socket.setproxy(SOCKS_TYPE, SOCKS_HOST, SOCKS_PORT)   
socket.connect((parsed.netloc, 3001)) 
r = remote.fromsocket(socket)

#Guess a number!
r.recvline()

#The number is in range 0 ~ 2^69
txt = r.recvline()
print(txt)
low = 0
pow = txt.decode()[-3:]
high = 2 ** int(pow)
print(int(pow), high)

#Your guess:
txt = r.recvuntil(b': ')
print(txt.decode())


#binary search
mid = ((low + high) // 2)
guess = mid
r.sendline(str(guess))
oracle = r.recvline().decode()
while('You are correct!' not in oracle):
    print(oracle)
    if oracle == 'Too small!\n':
        r.recvuntil(b': ')
        low = mid
    if oracle == 'Too big!\n':
        r.recvuntil(b': ')
        high = mid
    mid = ((low + high) // 2)
    guess = mid
    print(f'low : {low}, high : {high}, guess: {guess}')
    r.sendline(str(guess))
    oracle = r.recvline().decode()
#flag = r.recvline().decode()
r.interactive()






