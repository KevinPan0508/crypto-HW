#!/usr/local/bin/python3 -u

from secret import flagb1, p, g, serverPrivate
from utils import Server
from Cryptodome.Util.number import inverse, getStrongPrime


def main():
    bob = Server(flag1=flagb1, p=p, private=serverPrivate)
    bob.run()


if __name__ == "__main__":
    main()
