from ClassGroup import *
from Cryptodome.Util.number import getPrime
while True:
    p = getPrime(128)
    if p%8 == 7:
        break
d = -p
x = ClassGroup(d).generator()

print(x)