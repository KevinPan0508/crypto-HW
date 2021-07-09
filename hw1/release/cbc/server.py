#!/usr/sbin/python3

from Crypto.Cipher import AES
import sys
import binascii
import os
from myErrors import *
import secret

def pad(m):
    length = 16-len(m)%16
    return m+chr(length).encode()*length

def unpad(c):
    length = c[-1]
    for char in c[-length:]:
        if char!=length:
            raise paddingError('incorrect padding')
    return c[:-length]

def encrypt(m):
    aes = AES.new(secret.key,AES.MODE_CBC,secret.iv)
    return binascii.hexlify(aes.encrypt(pad(m))).decode()

def decrypt(c):
    aes = AES.new(secret.key,AES.MODE_CBC,secret.iv)
    return unpad(aes.decrypt(binascii.unhexlify(c))).decode()


def encrypt_message():
    global isTA
    identity = b'??'
    if isTA:
        identity = b'TA'
    try:
        print('The length of message can not exceed 16 bytes!')
        message =input('message(hex encoded) : ')
        message = binascii.unhexlify(message)
        if( len(message) <= 16 ):
            message = b'id=i_am_the_'+identity + b'||act=do_nothing||'+b'your_message_is:' + message
            print(encrypt(message))
        else:
            print('Your message is too long!')
        return
    except Exception as e:  
        print(e)
        return

def decrypt_message():
    try:
        message =input('message(hex encoded) : ')
        return
    except Exception as e:
        if e.__class__.__name__=='UnicodeDecodeError':
            print('Unicode Decode Error')
        else:
            print(e)
        return

def update_id():
    global isTA,canPrintFlag
    try:
        print('To update the identity, the decrypted message should be : id=[your_id]||act=[your_act]')
        message =input('give me the encrypted message : ')
        message = decrypt(message)
        messages = message.split('||')
        if(messages[0] == 'id=i_am_the_ta'):
            isTA = True
        if(messages[1] == 'act=printtheflag'):
            canPrintFlag = True
        
    except Exception as e:
        if e.__class__.__name__=='UnicodeDecodeError':
            print('Unicode Decode Error')
        else:
            print(e)

def menu():
    global isTA, canPrintFlag
    print(f"{' Simple padding oracle ':=^20}")
    if isTA:
        print("identity: TA")
    else:
        print("identity: ??")
    if canPrintFlag:
        print("I can print flag now!")
    print('1. encrypt message')
    print('2. decrypt message')
    print('3. update identity')
    print('4. print the flag')
    print('5. I give up!')
    print(f"{'':=^20}")

'''
if __name__=='__main__':
    isTA = False
    canPrintFlag = False
    while True:
        menu()
        choice = input('your choice : ').strip()
        try:
            choice=int(choice)
        except:
            print('Invalid Command')
            continue
        if choice==1:
            encrypt_message()
        elif choice==2:
            print(decrypt_message())
        elif choice==3:
            update_id()
        elif choice==4:
            if isTA and canPrintFlag:
                print(f'Congratulations, here is the flag : \n{secret.flag}')
            else:
                print('Only TA can print the flag!')
        elif choice==5:
            print('Goodbye')
            break
        else:
            print('Invalid Command')
'''