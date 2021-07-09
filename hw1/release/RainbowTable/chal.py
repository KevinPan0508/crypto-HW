from hashlib import sha512
from random import randint
from time import time

'''
Password list: https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt
Backup link: https://drive.google.com/file/d/1w9tl3HNYLkxIWG5knc4QlSA5dXX2fRh7/view?usp=sharing
SHA256: 1843265e3860a97f417b2236dfa332a0d93b38efef0fee1a0a291fdba5458478
'''

def mutate(s):
    tail = str(randint(0, 9999)).rjust(4, '0')
    return s + tail

def salted(s):
    return (s + "CNS2021").encode()

def hashfunc(s):
    return sha512(s).hexdigest()

with open("10-million-password-list-top-1000000.txt", 'r') as infile:
    passwords = infile.read().splitlines()

with open("flag.txt", 'r') as infile:
    flag, bonus_flag = infile.read().splitlines()

hint = mutate(passwords[randint(0, len(passwords)-1)])
print(f"[*] Example: sha512(salted({hint})) = {sha512(salted(hint)).hexdigest()}\n")

choices = set()
while len(choices) < 1000:
    choices.add(mutate(passwords[randint(0, len(passwords)-1)]))
challenge = [hashfunc(salted(choice)) for choice in choices]
print(f"[*] Challenge: {';'.join(challenge)}")

begin = time()
answer = input("[*] Please give me the passwords (separated with '<CNS>'): ").strip()
if time() - begin > 300:
    print("[!] Sorry, you are too slow")
    exit()

got_passwords = set(answer.split("<CNS>"))

if len(got_passwords) > 1000:
    print("[!] No cheating! Otherwise you will get a F :(")
    exit()

if got_passwords <= choices and len(got_passwords) >= 50:
    print(f"[*] Yeah! Here's the flag: {flag}")
    if len(got_passwords) >= 250:
        print(f"[*] Congratulation! Here's the bonus flag: {bonus_flag}")
else:
    print("[!] Sorry, no flag for you")