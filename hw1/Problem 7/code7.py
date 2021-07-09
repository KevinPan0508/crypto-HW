from pwn import *
from Cryptodome.Cipher import AES
import sys
import binascii
import os

cipher = '243c0d89d4e8eebae43c1aa219115b4364f88c485e808222f56fa095e68b1331856cbae6c179f53bb3046b93b39936890fc4a0eadea0e013d8130c4775d54dc8c493f1cdc62c523166b3ad49915ead45'
cipher_1 = cipher[:32]
cipher_2 = cipher[32:64]
cipher_3 = cipher[64:96]
cipher_4 = cipher[96:128]
cipher_5 = cipher[128:]
intermediate = '9567f2fdc17dee01b5156aadf5f92383'
iv = '796f75725f65766572796461795f6976'

def xor(x1, x2):
    result = ""
    for byte in range(0, len(x1)-1 ,2):
        byte_x1 = x1[byte]+x1[byte+1]
        byte_x2 = x2[byte]+x2[byte+1]
        xor = hex(int(byte_x1,16) ^ int(byte_x2,16)).replace('0x', '').zfill(2)
        result = result + xor
    return result

def padding_attack(c3, last_part):  
    p1 = binascii.hexlify(b'id=i_am_the_??||').decode()
    r = remote('cns.csie.org','8506')
    guess_p4_prum = c3
    for guess_byte in range(1,17):
        for byte in range(0,256):
            r.recvuntil(b'your choice :')
            r.sendline('2')
            padding = hex(guess_byte).replace('0x','').zfill(2) * guess_byte
            target_byte = c3[-2 * guess_byte:]
            if(guess_byte == 1):
                temp = hex(byte).replace('0x','').zfill(2)
            else:
                temp = hex(byte).replace('0x','').zfill(2) + guess_p4_prum[-2 * (guess_byte-1):]
            guess_byte_hex = xor(xor(target_byte,temp),padding)  
            payload = cipher_1 + cipher_2 + guess_p4_prum[:-2*guess_byte] + guess_byte_hex + last_part
            r.recvuntil(b'message(hex encoded) :')
            r.sendline(payload)
            txt = r.recvline().decode().strip('\n')
            if('PADDING ERROR' not in txt):
                guess_p4_prum = guess_p4_prum[:-2*guess_byte] + hex(byte).replace('0x','').zfill(2) + guess_p4_prum[-2 * guess_byte:][2:] 
                print(hex(byte).replace('0x','').zfill(2))
    return xor(xor(guess_p4_prum,cipher_3),p1) 

def get_construct_cipher(plain_byte, block, intermediate_vector):
    r = remote('cns.csie.org','8506')
    r.recvuntil(b'your choice :')
    r.sendline('1')
    r.recvuntil(b'message(hex encoded) :')
    p4 = binascii.hexlify(plain_byte).decode()
    r.sendline(p4)
    cipher = r.readline().decode().strip('\n').strip(' ')
    cipher_1 = cipher[:32]
    cipher_2 = cipher[32:64]
    cipher_3 = cipher[64:96]
    cipher_4 = cipher[96:128]
    cipher_5 = cipher[128:] 
    input = xor(xor(cipher_3, intermediate_vector),p4)
    r.recvuntil(b'your choice :')
    r.sendline('1')
    r.recvuntil(b'message(hex encoded) :')
    r.sendline(input)
    construct_cipher = r.readline().decode().strip('\n').strip(' ')
    if(block == 1):
        return construct_cipher[96:128]
    elif(block ==2 ):
        return construct_cipher[96:] 

def get_flag():
    cc1 = get_construct_cipher(b'id=i_am_the_ta||',1,iv)
    cc2 = get_construct_cipher(b'act=printtheflag',2,cc1)
    r = remote('cns.csie.org','8506')
    r.recvuntil(b'your choice :')
    r.sendline('3')
    r.recvuntil(b'give me the encrypted message :')
    r.sendline(cc1+cc2)
    r.recvuntil(b'your choice :')
    r.sendline('4')
    r.recvline()
    flag = r.recvline().decode().strip('\n')
    print(flag)

#print(padding_attack(cipher_3,cipher_1))
get_flag()