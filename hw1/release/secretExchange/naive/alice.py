#!/usr/local/bin/python3 -u

from secret import flaga1, flaga2
from utils import Client
from Cryptodome.Util.number import inverse, getStrongPrime


def main():
    alice = Client(flag1=flaga1, flag2=flaga2, p=getStrongPrime(1024))
    alice.run()


if __name__ == "__main__":
    main()
