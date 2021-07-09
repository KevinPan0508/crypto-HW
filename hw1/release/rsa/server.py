#! /usr/bin/env python3

import os
from Cryptodome.Util.number import getStrongPrime
from secret import *

class rsa_key:
    def __init__(self):
        self.e = 3
        self.p = getStrongPrime(512, 3)
        self.q = getStrongPrime(512, 3)
        self.n = self.p * self.q
        self.phi = (self.p-1) * (self.q-1)
        self.d = pow(self.e, -1, self.phi)

def encrypt(m, key):
    return pow(m, key.e, key.n)

def decrypt(c, key):
    return pow(c, key.d, key.n)

def valid_input():
    while True:
        num = input('Please give me a positive integer: ')
        try:
            num = int(num)
            return num%(1<<1024)
        except:
            pass

def getflag1():
    key = rsa_key()
    c = encrypt(int.from_bytes(flag1.encode(), 'big'), key)
    print('This is the first encrpyted flag. Oops! It seems too short!')
    print(f'encrypted flag: {c}')
    return

def getflag2():
    key = rsa_key()
    c = encrypt(int.from_bytes(flag2.encode(), 'big'), key)
    print('This is the second encrypted flag. This time, I made the flag long enough. HAHAHA!!!')
    print(f'encrypted flag: {c}')
    print(f'Umm... let me give you the modulus n: {key.n}')
    return

def getflag3():
    key = rsa_key()
    flag = int.from_bytes(flag3.encode(), 'big')
    print('Let me encrypt something for you~')
    m1 = valid_input()
    c1 = encrypt(m1, key)
    print(f'Here is your encrypted number: {c1}')
    print('This is the third encrypted flag. Can you get it?')
    c = encrypt(flag, key)
    print(f'encrypted flag: {c}')
    return

def getflag4():
    key = rsa_key()
    flag = int.from_bytes(flag4.encode(), 'big')
    print('Since e is so small, let\'s use d to encrypt.')
    print('Let me encrypt something for you~')
    m1 = valid_input()
    c1 = decrypt(m1, key)
    print(f'Here is your encrypted number: {c1}')
    print('I can encrypt another one~')
    m2 = valid_input()
    c2 = decrypt(m2, key)
    print(f'Here is your decrypted number: {c2}')
    print('This is the last encrypted flag. Can you get it?')
    c = decrypt(flag, key)
    print(f'encrypted flag: {c}')
    return

def menu():
    print('===================')
    print(' 1. flag1(2%)      ')
    print(' 2. flag2(3%)      ')
    print(' 3. flag3(5%)      ')
    print(' 4. flag4(bonus 5%)')
    print(' 5. exit           ')
    print('===================')

if __name__ == '__main__':
    while True:
        menu()
        choice = input('Your choice: ').strip()
        try:
            choice = int(choice)
        except:
            print('Invalid Choice')
            continue
        if choice == 1:
            getflag1()
        elif choice == 2:
            getflag2()
        elif choice == 3:
            getflag3()
        elif choice == 4:
            getflag4()
        elif choice == 5:
            break
        else:
            print('Invalid Choice')


