#!/usr/local/bin/python3 -u
# -*- coding: latin-1 -*-
import os
import sys
import hmac
import time

from secrets import admin_password, flag, admin_ntlm_hash
from des import *

from binascii import unhexlify, hexlify
from Cryptodome.Util.number import long_to_bytes, bytes_to_long

minimal = [16]
total_accounts = {b"admin": admin_password}
total_hashes = {b"admin": admin_ntlm_hash}

def read_more(f, now, length):
    ret = b""
    length -= now
    now = 0
    while now < length:
        print (now, length, file=sys.stderr)
        ret += b"\n"
        if now == length - 1:
            break
        ret += f.readline()[:-1]
        now = len(ret)
    return ret


def panic(ret):
    print(ret)
    raise NotImplementedError


def register():
    try:
        user_account = input("Account: ").encode()
        assert b"admin" not in user_account
        user_password = input("Password: ").encode()
        total_accounts[user_account] = user_password
    except:
        panic("Somthing went wrong...")

def login():
    user_account = input("Account: ").encode().strip(b"\n")
    if user_account not in total_accounts:
        print("User does not exist")
        return
    user_password = total_accounts[user_account]
    if standard_ntlmv2_authentication(user_password):
        if user_account == b"admin":
            print(f"Hi admin! Here is our flag: {flag}")
        else:
            ntlm_hash = bytes.fromhex(MD4(user_password).hexdigest())
            total_hashes[user_account] = ntlm_hash
            print(f"Hi {user_account}, you are now in the list, please check it")
            print(total_hashes)

def standard_ntlmv2_authentication(password):
    with open(sys.stdin.fileno(), "rb", closefd=False) as f:
        type1_msg = f.readline()[:-1]
        while len(type1_msg) < minimal[0]:
            type1_msg += b"\n" + f.readline()[:-1]
        # ...
    return True

def logout():
    print(f"Byte~")
    exit(255)

def menu():
    print ("Please login as admin to get flag")
    print ("To start, register a normal account and try to login")
    print ("1. register")
    print ("2. login")
    print ("3. exit")

funcs = [register, login, logout]

if __name__ == "__main__":
    while True:
        menu()
        try:
            option = int(input('option >> '))
            assert option in [1, 2, 3]
        except:
            panic("Valid options only include 1 or 2 or 3")
        funcs[option-1]()



