#!/usr/bin/python3 -u
import os
import random

from enum import Enum
from Cryptodome.Cipher import AES


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
    def __init__(self, flag1, flag2, g=2, p=None):
        self.state = State.Initial
        self.g = g
        self.p = p

        self.flag1 = flag1
        self.flag2 = flag2

    # long and tedious state machine
    def run(self):
        while True:
            if self.state == State.Initial:
                # send p, g, g^a
                # generate private key
                self.private = random.randint(2, self.p - 2)
                self.public = pow(self.g, self.private, self.p)

                # send parameters
                self.send("p: ", self.p)
                self.send("g: ", self.g)
                self.send("public: ", self.public)

                # state transition
                self.state = State.WaitKey

            elif self.state == State.WaitKey:
                # read g^b, AES iv, send flag1
                # read server's public key
                try:
                    serverPublic = int(self.read("public: "))
                    assert 1 <= serverPublic < self.p
                except:
                    self.send("Something went wrong...", "")
                    exit(255)

                # generate session key
                mask = (1 << 128) - 1
                self.sessionKey = (
                    pow(serverPublic, self.private, self.p) & mask
                ).to_bytes(16, "big")

                # generate cipher kits
                try:
                    self.iv = bytes.fromhex(self.read("iv: "))
                    assert len(self.iv) == 16
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
    def __init__(self, flag1):
        self.state = State.WaitKey

        self.flag1 = flag1

    def run(self):
        while True:
            if self.state == State.WaitKey:
                # read p, g, g^a, send g^b, AES's iv
                # read client's public key
                try:
                    self.p = int(self.read("p: "))
                    self.g = int(self.read("g: "))
                    clientPublic = int(self.read("public: "))
                    assert 1 <= clientPublic < self.p
                except:
                    self.send("Something went wrong...", "")
                    exit(255)

                # generate private key
                self.private = random.randint(2, self.p - 2)
                self.public = pow(self.g, self.private, self.p)

                # send public key
                self.send("public: ", self.public)

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
                self.send("iv: ", self.iv.hex())

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
