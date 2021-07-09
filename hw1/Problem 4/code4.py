from pwn import *
from caesar import *
from padding import *
from zigzag import *
from bacon import *
from test import *

r = remote('cns.csie.org','17277')
#warmup1
txt = r.recvuntil(b'[>]:')
print(txt.decode().replace('\\n',''))
r.sendline('2')
#warmup1
#warmup2
txt = r.recvline()
print(txt.decode().replace('\\n',''))
txt = r.recvline()
print(txt.decode().replace('\\n',''))
txt = r.recvuntil(b'[+] ')
txt  = r.recvuntil(b'[>]:')
answer = txt.decode().replace('text = ','').replace('[>]:','').rstrip('\n')
print(txt.decode().replace('\\n',''))
r.sendline(answer)
#warmup2
#round1
txt  = r.recvuntil(b'[+]')
print(txt.decode().replace('\\n',''))
txt  = r.recvuntil(b'[+]')
cipher = txt.decode().replace(' c1 = ','').replace('[+]','').rstrip('\n')
list = []
for i in range(1,27):
    plain_text = caesar_decrypt(cipher,i)
    list.append(plain_text)
    print('index = {0}, string = {1}'.format(i-1,plain_text))
choice = input('choose your plain text index number\n')
plain_text = list[int(choice)]
txt  = r.recvuntil(b'[>]:')
r.sendline(plain_text)
#round1
#round2
txt  = r.recvuntil(b' c1 = ')
print(txt.decode().replace('\\n',''))
txt = r.recvuntil(b'[+]')
print(txt.decode().replace('\\n',''))
key = txt.decode().replace('[+]','').strip('\n')
txt  = r.recvuntil(b'Eve : ')
print(txt.decode().replace('\\n',''))
txt  = r.recvuntil(b'Alice : ')
cipher = txt.decode().replace('Alice : ','').strip('\n')
txt  = r.recvuntil(b'[+]')
text = txt.decode().replace('[+]','').strip('\n')
print(txt.decode().replace('\\n',''))
answer = padding_decrypt(text, key, cipher.encode())
txt  = r.recvuntil(b'[>]:')
print(txt.decode().replace('\\n',''))
r.sendline(answer)
#round2
#round3
txt = r.recvuntil(b'c2 = ')
print(txt.decode().replace('\\n',''))
txt = r.recvuntil(b'[+]')
plain = txt.decode().replace('[+]','').strip('\n')
print(txt.decode().replace('\\n',''))
txt  = r.recvuntil(b'[>]:')
answer = bacon_encrypt(plain)
print(txt.decode().replace('\\n',''))
r.sendline(answer)
#round3
#round4
txt = r.recvline()
print(txt.decode().replace('\\n',''))
txt = r.recvuntil('c1 = ')
print(txt.decode().replace('\\n',''))
txt = r.recvuntil('[+]')
print(txt.decode().replace('\\n',''))
cipher = txt.decode().replace('[+]','').strip('\n')
txt = r.recvuntil('m1 = ')
print(txt.decode().replace('\\n',''))
txt = r.recvuntil('[+]')
print(txt.decode().replace('\\n',''))
plain = txt.decode().replace('[+]','').strip('\n')
txt = r.recvuntil('c2 = ')
print(txt.decode().replace('\\n',''))
txt = r.recvuntil('[+]')
print(txt.decode().replace('\\n',''))
quiz = txt.decode().replace('[+]','').strip('\n')
txt = r.recvuntil('[>]:')
print(txt.decode().replace('\\n',''))
list = []
for i in range(3,20):
    zigzag = zigzag_build(len(cipher),i)
    if(zigzag_decrypt(zigzag, cipher) == plain):
        stairs = i
        break
zigzag = zigzag_build(len(quiz),stairs)
answer = zigzag_decrypt(zigzag, quiz)
r.sendline(answer)
#round 4
#Here comes the flag
txt = r.recvuntil('}')
print(txt.decode().replace('\\n',''))





