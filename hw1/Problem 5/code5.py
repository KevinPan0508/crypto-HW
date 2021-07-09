#from Cryptodome.Util.number import getStrongPrime
from pwn import *
from numpy import cbrt
from libnum import *
from decimal import *
import gmpy2
#1
cipher_1 = 951828082032511618701999945132660495209670382840341658105893214146100320221193574011767196679751736141033354034943938396607494792024108235848414529893
#1
#2
c2_1 = 103640558567784999813172398098952425487324338619206124045302299642014728307392465723785988927667399691710449374040444027652548526586942887935438696829696372732031044323511460267144632500110550935966894267178714817437696909504355185487320910378226724250241222376152760632046787568162127638474815717665243097672
n1 = 130053182131508701713556723667043786034670413795274916303064294832792212864586066744151865269062236266803870655373500614727878492042459010612151112012097579551923337591262646736063300166011013609937642411920525413450143031975510782540618550033606243151065834355701795446956945151746512056049407426219044161209
c2_2 = 12629024335509381680755932832473069897123490208065373003399984196108298446393111445624106669141155933612965710077010332815055867785541402501215590453356632417696290507366378643075092224981770731659615197901543287237145589354635181599607250637191690480575602786704636915816669831430382376071937213615120237930
n2 = 135569874718596184923529349971333884554268881257737040225716173559290578200070066041854551045142532396469407102284583737758241554741879558659461082780831344570418621804429076456466226381823228289675465886931773136797747889629930777785562341327667164383346867294219907764526392393624623180504827481544879654761
c2_3 = 25959859713498282762904441156125995487538749372158391439976969962436433024297345976008920926690177885486204104978855496548447470207592598067160160547587449064109061737881291603412771328637519998648860388310726358497052725335707278755927617506978843828687342798088699392482406060667194664403294038608004926104
n3 = 155704628636717286790646900827315457892785292689763057303227790990873772505812497688867647982398259410937681753208159064710335919568278886257929417283238262556735444875412922129342528387525968352425020622183198838919660386882217631323219901283222799314790727352772235947200113255749386650644197540278631716947
#2  
#3
'''
猜測 N 為 308 or 309 位數
c1 = input ** 3 (mod N)
c2 = flag3 ** 3 (mod N)
'''

#3

def length(x):
    return len(str(x))


def cbrt(x):
    x = str(x)
    minprec = 3
    if len(x) > minprec: getcontext().prec = len(x)
    else:                getcontext().prec = minprec
    x = Decimal(x)
    power = Decimal(1)/Decimal(3)
    answer = x**power
    ranswer = answer.quantize(Decimal('1.'), rounding=ROUND_UP)
    diff = x - ranswer**Decimal(3)
    if diff == Decimal(0):
        return ranswer
    else:
        return answer
def flag1(): 
    plain_byte = nroot(cipher_1, 3)
    answer = plain_byte.to_bytes(len(str(plain_byte)), 'big').decode()
    print(answer)  
'''
def flag2(n1,n2,n3,m1,m2,m3):
    M = n1 * n2 * n3
    m1 = n2 * n3 
    m2 = n1 * n3 
    m3 = n1 * n2
    t1 = pow(m1, -1, n1)
    t2 = pow(m2, -1, n2)
    t3 = pow(m3, -1, n3)
    while True:
        guess_cube = (m1*c2_1*t1 + m2*c2_2*t2 + m3*c2_3*t3) % M 
        print(guess_cube)
        guess_plain = int(str(cbrt(guess_cube)))
        answer = guess_plain.to_bytes(len(str(guess_plain)), 'big').decode()
        if('CNS{' in answer):
            print(answer)
            break
'''

def flag2(n1,n2,n3,c1,c2,c3):
    M = gmpy2.mpz(n1) * gmpy2.mpz(n2) * gmpy2.mpz(n3)
    m1 = gmpy2.mpz(n2) * gmpy2.mpz(n3) 
    m2 = gmpy2.mpz(n1) * gmpy2.mpz(n3) 
    m3 = gmpy2.mpz(n1) * gmpy2.mpz(n2)
    t1 = gmpy2.invert(m1, n1)
    t2 = gmpy2.invert(m2, n2)
    t3 = gmpy2.invert(m3, n3)
    while True:
        guess_cube = (m1*gmpy2.mpz(c1)*t1 + m2*gmpy2.mpz(c2)*t2 + m3*gmpy2.mpz(c3)*t3) % M 
        guess_plain = int(str(gmpy2.iroot(guess_cube,3)[0]))
        answer = guess_plain.to_bytes(len(str(guess_plain)), 'big').decode()
        if('CNS{' in answer):
            print(answer)
            break

    
def getn():
    test = gmpy2.mpz(5067920000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000)
    r = remote('cns.csie.org', '8503')
    r.recvuntil(b'Your choice: ')
    r.sendline('3')
    r.recvuntil(b'Please give me an integer: ')
    r.sendline(str(test))
    r.recvuntil(b'Here is your encrypted number: ')
    txt = r.recvuntil(b'This is the third encrypted flag. Can you get it?')
    cipher_1 = txt.decode().replace('This is the third encrypted flag. Can you get it?', '').strip('\n')
    r.recvuntil(b'encrypted flag: ')
    txt = r.recvuntil(b'===================')
    cipher_2 = txt.decode().replace('===================', '').strip('\n')
    cube = test ** gmpy2.mpz(3)
    while(cube == gmpy2.mpz(cipher_1)):
        cube = test ** gmpy2.mpz(3)
        r.recvuntil(b'Your choice: ')
        r.sendline('3')
        r.recvuntil(b'Please give me an integer: ')
        r.sendline(str(test))
        r.recvuntil(b'Here is your encrypted number: ')
        txt = r.recvuntil(b'This is the third encrypted flag. Can you get it?')
        cipher_1 = txt.decode().replace('This is the third encrypted flag. Can you get it?', '').strip('\n')
        r.recvuntil(b'encrypted flag: ')
        txt = r.recvuntil(b'===================')
        cipher_2 = txt.decode().replace('===================', '').strip('\n')
        test = test + 1
    guess_n =  cube - gmpy2.mpz(cipher_1)
    guess_cipher_1 = (gmpy2.mpz(test) ** gmpy2.mpz(3))% gmpy2.mpz(guess_n)
    if(cube > gmpy2.mpz(guess_n) and guess_cipher_1 == gmpy2.mpz(cipher_1)):
        return guess_n, test, cipher_1, cipher_2

def find_factor(x):
    for i in range(2, gmpy2.iroot(x,2)[0]):
        if(gmpy2.mpz(x) % gmpy2.mpz(i) == 0):
            print(i)

while(1):
    try:
        n3_1,test_1,cipher_1_1,cipher_1_2 = getn()
        try: 
            n3_2, test_2, cipher_2_1, cipher_2_2 = getn()
            try: 
                n3_3, test_3, cipher_3_1, cipher_3_2 = getn()
                break
            except TypeError:
                continue
        except TypeError:
            continue
    except TypeError:
        continue
flag1()
flag2(n1,n2,n3,c2_1,c2_2,c2_3)
flag2(n3_1,n3_2,n3_3,cipher_1_2,cipher_2_2,cipher_3_2)