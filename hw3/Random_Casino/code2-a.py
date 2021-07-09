import random
import binascii
import os
from pwn import *

def check_random(contributions):
    randomness = 0
    for contribution in contributions:
        randomness ^= int.from_bytes(contribution, 'big')
    random.seed(randomness)
    if(random.random() > 0.5):
        return binascii.hexlify((0).to_bytes(256, 'big'))
    else:
        while(1):
            temp = randomness
            final = os.urandom(256)
            temp ^= int.from_bytes(final, 'big')
            random.seed(temp)
            test = random.random()
            if(test > 0.5):
                return binascii.hexlify(final)


r = remote("cns.csie.org", "7680")
#first try
txt = r.recvuntil("Current money: ")
txt = r.recvuntil("G")
current = int(txt.decode().strip('\n').replace('G',''))
txt = r.recvuntil('Your choice: ')
r.sendline(b'1')
contribution = []
for i in range(9):
    txt = r.recvline().decode().strip('\n').replace('Contribution: ','')
    txt = binascii.unhexlify(txt)
    contribution.append(txt)
txt = r.recvuntil("Give me your contribution (at most 256 bytes) in hexadecimal: ")
r.sendline(check_random(contribution))
while(current != 200):
    txt = r.recvuntil("Current money: ")
    txt = r.recvuntil("G")
    current = int(txt.decode().strip('\n').replace('G',''))
    print(f'current = {current}G')
    txt = r.recvuntil('Your choice: ')
    r.sendline(b'1')
    contribution = []
    for i in range(10):
        txt = r.recvline().decode().strip('\n').replace('Contribution: ','')
        txt = binascii.unhexlify(txt)
        contribution.append(txt)
    txt = r.recvuntil("Give me your contribution (at most 256 bytes) in hexadecimal: ")
    r.sendline(check_random(contribution))
r.interactive()




