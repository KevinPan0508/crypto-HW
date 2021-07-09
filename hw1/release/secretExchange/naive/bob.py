#!/usr/local/bin/python3 -u

from secret import flagb1
from utils import Server
from Cryptodome.Util.number import inverse, getStrongPrime


def main():
    bob = Server(flag1=flagb1)
    bob.run()


if __name__ == "__main__":
    main()
