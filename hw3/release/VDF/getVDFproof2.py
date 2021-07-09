#!/usr/bin/python3

from ClassGroup import ClassGroup, Form
from Cryptodome.Util.number import getPrime
import random
import VDF     # the module VDF is not provided
import secret

def generateChallenge():
    d = -170141183460469231731687303715884105727
    T = random.randint(1<<100, 1<<101)
    L = getPrime(128)
    return d, T, L

def parseInput():
    try:
        y = list(map(int, input("y = ").strip().split()))
    except:
        raise BaseException("Invalid Form")
    if len(y) != 3:
        raise BaseException("Invalid Form")

    try:
        proof = list(map(int, input("proof = ").strip().split()))
    except:
        raise BaseException("Invalid Form")
    if len(proof) != 3:
        raise BaseException("Invalid Form")
    
    return y, proof

def discriminant(x):
    return x[1]*x[1] - 4*x[0]*x[2]

def verify(d, T, L, y, proof):
    if discriminant(y) != d:
        raise BaseException("Wrong discriminant")
    if discriminant(proof) != d:
        raise BaseException("Wrong discriminant")
    x = ClassGroup(d).generator()
    y = Form(y[0], y[1], y[2])
    proof = Form(proof[0], proof[1], proof[2])
    return VDF.Verify(d, x, T, L, y, proof)


if __name__ == "__main__":
    d, T, L = generateChallenge()
    print(f"d = {d}")
    print(f"T = {T}")
    print(f"L = {L}")
    print("x = Classgroup(d).getForm(a, b)")
    print("Give me y = x ^ (1<<T)")
    print("and a proof = x ^ (1<<T)//L")
    print("I will check that y == (proof ^ L) * (x ^ (1<<T)%L)")
    y, proof = parseInput()
    if verify(d, T, L, y, proof):
        print(f"This is your flag: {secret.flag}")
        print("Give me another y and proof?")
        _y, _proof = parseInput()
        if y != _y and verify(d, T, L, _y, _proof):
            print(f"This is your flag: {secret.flag2}")
        else:
            print("Invalid proof")
    else:
        print("Invalid proof")