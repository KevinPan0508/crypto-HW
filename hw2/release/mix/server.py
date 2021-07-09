import numpy as np
import secret
import time

table = []

np.random.seed(int(time.time())*secret.m%secret.random)

def gen_table():
    for i in range(5):
        tmp = np.random.randint(2,size=5)
        while(tmp[i] == 1 or np.sum(tmp) < 1):
            tmp = np.random.randint(2,size=5)
        table.append(list(tmp))

#make sure there is a cycle
good_table = False
while( not good_table):
    table = []
    gen_table()
    good_table = True
    t = np.array(table)
    for i in range(5):
        if(np.sum(t[:,i]) == 0):
            good_table = False
            break

com = []
for i in range(5):
    for j in range(i+1,5):
        for k in range(j+1,5):
            com.append([i,j,k])


rel_list = []
for c in com:
    s1,s2,s3 = c
    for r1 in range(5):
        if table[s1][r1] == 0:
            continue
        for r2 in range(5):
            if table[s2][r2] == 0:
                continue
            for r3 in range(5):
                if table[s3][r3] == 0:
                    continue
                #senders >> receivers
                rel_str = "s{} s{} s{} >> ".format(s1+1,s2+1,s3+1)
                r_set = set()
                r_set.add(r1)
                r_set.add(r2)
                r_set.add(r3)
                for r in r_set:
                    rel_str += "s{} ".format(r+1)

                rel_list.append(rel_str)
np.random.shuffle(rel_list)
for r in rel_list:
    print(r)

print("A packet should be like '[receiver]||[YOUR MESSAGE]'")
print("For example: s2||hello")
packet = input("Please give me the packet: ")

jump_set = set()
prev = None
for i in range(7):
    if packet[0] != 's' or (not packet[1].isdigit()) or packet[2:4] != "||":
        print("Wrong format!")
        exit(-1)
    recv = int(packet[1]) - 1
    if recv > 4 or recv < 0:
        print("Wrong receiver!")
        exit(-1)
    if prev != None:
        if table[prev][recv] == 0:
            print("packet can't reach!")
            exit(-1)
    prev = recv
    packet = packet[4:]
    jump_set.add(recv)
    if len(jump_set) == 5:
        if packet == "print the flag":
            if(recv != 4):
                print("I can't print the flag!")
                exit(-1)
            print(f'Congratulations, here is the flag : \n{secret.flag}')
        else:
            print("Wrong message!")
        break
