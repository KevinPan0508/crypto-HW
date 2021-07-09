#!/usr/local/bin/python3 -u

from secret import flaga1, flaga2, p, g, serverPublic
from utils import Client
from Cryptodome.Util.number import inverse, getStrongPrime


def main():
    alice = Client(flag1=flaga1, flag2=flaga2, p=p, serverPublic=serverPublic)
    alice.run()


if __name__ == "__main__":
    main()
