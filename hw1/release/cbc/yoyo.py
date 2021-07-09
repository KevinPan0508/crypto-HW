from pwn import *
from Cryptodome.Cipher import AES
import sys
import binascii
import os

#test_cipher = encrypt(plain_text)
#test_cipher_1 = test_cipher[:32] 
#test_cipher_2 = test_cipher[32:64] 
#test_cipher_3 = test_cipher[64:96]  
#test_cipher_4 = test_cipher[96:128]  
#test_cipher_5 = test_cipher[128:] 
plain_text = b'id=i_am_the_??||' + b'act=do_nothing||'+b'your_message_is:' + b'id=i_am_the_TA||'
p1 = binascii.hexlify(b'id=i_am_the_??||')
test_key = b'6250655368566D597033733676397924'
iv = 'aa' * 16

def pad(m):
    length = 16-len(m)%16
    return m+chr(length).encode()*length

def unpad(c):
    length = c[-1]
    for char in c[-length:]:
        if char!=length:
            raise NameError('incorrect padding')
    return c[:-length] 

def encrypt(m):
    aes = AES.new(test_key,AES.MODE_CBC,iv = bytes.fromhex(iv))
    return binascii.hexlify(aes.encrypt(pad(m))).decode()

def decrypt(c):
    aes = AES.new(test_key,AES.MODE_CBC,iv = bytes.fromhex(iv))
    #return unpad(aes.decrypt(binascii.unhexlify(c)))
    return aes.decrypt(binascii.unhexlify(c))


def xor(x1, x2):
    result = ""
    for byte in range(0, len(x1)-1 ,2):
        byte_x1 = x1[byte]+x1[byte+1]
        byte_x2 = x2[byte]+x2[byte+1]
        xor = hex(int(byte_x1,16) ^ int(byte_x2,16)).replace('0x', '').zfill(2)
        result = result + xor
    return result

def get_p4_prum(c3,test_cipher_1, test_cipher_2, test_cipher_3, test_cipher_4, test_cipher_5):  
    guess_p4_prum = c3
    for guess_byte in range(1,17):
        for byte in range(0,256):
            padding = hex(guess_byte).replace('0x','').zfill(2) * guess_byte
            target_byte = c3[-2 * guess_byte:]
            if(guess_byte == 1):
                temp = hex(byte).replace('0x','').zfill(2)
            else:
                temp = hex(byte).replace('0x','').zfill(2) + guess_p4_prum[-2 * (guess_byte-1):]
            guess_byte_hex = xor(xor(target_byte,temp),padding)  
            payload = test_cipher_1 + test_cipher_2 + guess_p4_prum[:-2*guess_byte] + guess_byte_hex + test_cipher_5
            try:
                decrypt(payload)
                guess_p4_prum = guess_p4_prum[:-2*guess_byte] + hex(byte).replace('0x','').zfill(2) + guess_p4_prum[-2 * guess_byte:][2:] 
                print(hex(byte).replace('0x','').zfill(2))
            except NameError:
                continue
    return guess_p4_prum

def xor(x1, x2):
    result = ""
    for byte in range(0, len(x1)-1 ,2):
        byte_x1 = x1[byte]+x1[byte+1]
        byte_x2 = x2[byte]+x2[byte+1]
        xor = hex(int(byte_x1,16) ^ int(byte_x2,16)).replace('0x', '').zfill(2)
        result = result + xor
    return result    

def get_construct_cipher_1(plain_byte,block, intermediate_vector):
    cipher = encrypt(b'id=i_am_the_??||' + b'act=do_nothing||'+b'your_message_is:' + plain_byte)
    p4 = binascii.hexlify(plain_byte).decode()
    cipher_1 = cipher[:32]
    cipher_2 = cipher[32:64]
    cipher_3 = cipher[64:96]
    cipher_4 = cipher[96:128]
    cipher_5 = cipher[128:] 
    input = binascii.unhexlify(xor(xor(cipher_3, intermediate_vector),p4))
    construct_cipher = encrypt(b'id=i_am_the_??||' + b'act=do_nothing||'+b'your_message_is:' + input)
    if(block == 1):
        return construct_cipher[96:128]
    elif(block ==2 ):
        return construct_cipher[96:]

def get_construct_cipher_2(plain_byte,block, intermediate_vector):
    cipher = encrypt(b'id=i_am_the_??||' + b'act=do_nothing||'+b'your_message_is:' + plain_byte)
    p4 = binascii.hexlify(plain_byte).decode()
    cipher_1 = cipher[:32]
    cipher_2 = cipher[32:64]
    cipher_3 = cipher[64:96]
    cipher_4 = cipher[96:128]
    cipher_5 = cipher[128:] 
    input = binascii.unhexlify(xor(xor(cipher_3, intermediate_vector),p4))
    construct_cipher = encrypt(b'id=i_am_the_??||' + b'act=do_nothing||'+b'your_message_is:' + input)
    return construct_cipher[96:]