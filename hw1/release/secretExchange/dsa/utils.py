#!/usr/bin/python3 -u
import os
import random

from enum import Enum
from hashlib import sha512
from Cryptodome.Cipher import AES
from Cryptodome.Util.number import GCD, inverse


class State(Enum):
    Initial = 0
    WaitKey = 1
    WaitMessage = 2
    Finish = 3


class Station:
    def read(self, prefix: str):
        content = input().strip()
        assert content.startswith(prefix)
        assert isinstance(content, str)
        return content[len(prefix):]

    def send(self, prefix: str, content):
        if isinstance(content, int):
            content = str(content)

        print(prefix + content)


class Client(Station):
    def __init__(self, flag1, flag2, g=2, p=None, serverPublic=None):
        self.state = State.Initial
        self.g = g
        self.p = p
        self.serverPublic = serverPublic

        self.byteLength = (self.p.bit_length() + 7) // 8

        self.flag1 = flag1
        self.flag2 = flag2

    def checkSignature(self, content, signature):
        if isinstance(content, int):
            content = content.to_bytes(self.byteLength, "big")
        elif isinstance(content, str):
            content = content.encode()
        assert isinstance(content, bytes)

        # sanity check
        r, s = signature
        assert 0 < r < self.p
        assert 0 < s < self.p - 1

        # verify signature
        contentHash = int.from_bytes(sha512(content).digest(), "big")
        left = pow(self.g, contentHash, self.p)
        right = pow(self.serverPublic, r, self.p) * pow(r, s, self.p) % self.p
        assert left == right

    # long and tedious state machine
    def run(self):
        while True:
            if self.state == State.Initial:
                # send g^a
                # generate private key
                self.private = random.randint(2, self.p - 2)
                self.public = pow(self.g, self.private, self.p)

                # send parameters
                self.send("public: ", self.public)

                # state transition
                self.state = State.WaitKey

            elif self.state == State.WaitKey:
                # read g^b, AES iv, send flag1
                # read server's public key
                try:
                    serverReceivedPublic = int(self.read("receivedPublic: "))
                    r = int(self.read("r: "))
                    s = int(self.read("s: "))
                    assert serverReceivedPublic == self.public
                    self.checkSignature(serverReceivedPublic, (r, s))
                except Exception as e:
                    print(e)
                    self.send("Something went wrong...", "")
                    exit(255)

                # generate session key
                mask = (1 << 128) - 1
                self.sessionKey = (
                    pow(self.serverPublic, self.private, self.p) & mask
                ).to_bytes(16, "big")

                # generate cipher kits
                try:
                    self.iv = bytes.fromhex(self.read("iv: "))
                    r = int(self.read("r: "))
                    s = int(self.read("s: "))
                    assert len(self.iv) == 16
                    self.checkSignature(self.iv, (r, s))
                except:
                    print("Something went wrong...")
                    exit(255)

                self.encrypter = AES.new(
                    key=self.sessionKey, mode=AES.MODE_CBC, iv=self.iv
                )
                self.decrypter = AES.new(
                    key=self.sessionKey, mode=AES.MODE_CBC, iv=self.iv
                )

                # send flag1
                cipher = self.encrypter.encrypt(self.flag1)
                self.send("flag1: ", cipher.hex())

                # state transition
                self.state = State.WaitMessage

            elif self.state == State.WaitMessage:
                # read flag, send flag
                _ = self.read("flag1: ")
                cipher = self.encrypter.encrypt(self.flag2)
                self.send("flag2: ", cipher.hex())

                # state transition
                self.state = State.Finish

            else:
                break


class Server(Station):
    def __init__(self, flag1, g=2, p=None, private=None):
        self.state = State.WaitKey
        self.g = g
        self.p = p
        self.private = private
        self.public = pow(self.g, self.private, self.p)

        self.byteLength = (self.p.bit_length() + 7) // 8

        while True:
            self.k = random.randint(2, self.p - 2)
            if GCD(self.k, self.p - 1) == 1:
                break

        self.flag1 = flag1

    def calculateSignature(self, content):
        if isinstance(content, int):
            content = content.to_bytes(self.byteLength, "big")
        elif isinstance(content, str):
            content = content.encode()
        assert isinstance(content, bytes)

        contentHash = int.from_bytes(sha512(content).digest(), "big")
        r = pow(self.g, self.k, self.p)
        s = (
            (contentHash - self.private * r)
            * inverse(self.k, self.p - 1)
            % (self.p - 1)
        )
        return r, s

    def run(self):
        while True:
            if self.state == State.WaitKey:
                # read g^a, send g^a, signature(g^a), AES's iv, signature(AES's iv)
                # read client's public key
                try:
                    clientPublic = int(self.read("public: "))
                    assert 1 <= clientPublic < self.p
                except:
                    self.send("Something went wrong...", "")
                    exit(255)

                # send public key ack and signature
                r, s = self.calculateSignature(clientPublic)
                self.send("receivedPublic: ", clientPublic)
                self.send("r: ", r)
                self.send("s: ", s)

                # generate session key
                mask = (1 << 128) - 1
                self.sessionKey = (
                    pow(clientPublic, self.private, self.p) & mask
                ).to_bytes(16, "big")

                # generate cipher kits
                self.iv = os.urandom(16)
                self.encrypter = AES.new(
                    key=self.sessionKey, mode=AES.MODE_CBC, iv=self.iv
                )
                self.decrypter = AES.new(
                    key=self.sessionKey, mode=AES.MODE_CBC, iv=self.iv
                )

                # send AES's iv
                r, s = self.calculateSignature(self.iv)
                self.send("iv: ", self.iv.hex())
                self.send("r: ", r)
                self.send("s: ", s)

                # state transition
                self.state = State.WaitMessage

            elif self.state == State.WaitMessage:
                # read flag, send flag
                _ = self.read("flag1: ")
                cipher = self.encrypter.encrypt(self.flag1)
                self.send("flag1: ", cipher.hex())

                # state transition
                self.state = State.Finish

            else:
                break
