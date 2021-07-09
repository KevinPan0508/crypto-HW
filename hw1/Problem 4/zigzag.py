
def list_modified(List, x, y, character):
    List[y][x] = character

def list_initialize(x_length,y_length):
    list = [[None for i in range(x_length)] for j in range(y_length)]
    return list
'''
def zigzag_build(cipher,stairs):
    list = list_initialize(len(cipher), stairs)
    current_x, current_y = 0, 0
    flag = 1
    step = stairs - 1
    list_modified(list,0, current_y, cipher[0])
    while(current_x < len(cipher)):
        if(step != 0):
            if(flag == 1):
                current_y += 1
                step -= 1
            else:
                current_y -= 1
                step -= 1
            current_x += 1
        else:
            if(step == 0):
                flag = (flag + 1)%2
                step = 3
        if(current_x == len(cipher)):
            break
        list_modified(list,current_x, current_y, cipher[current_x])
    return list   
'''
def zigzag_build(length,stairs):
    list = list_initialize(length, stairs)
    current_x, current_y = 0, 0
    number = 0
    flag = 1
    step = stairs - 1
    list_modified(list,0, current_y, 0)
    while(current_x < length):
        if(step != 0):
            if(flag == 1):
                current_y += 1
                step -= 1
            else:
                current_y -= 1
                step -= 1
            current_x += 1
        else:
            if(step == 0):
                flag = (flag + 1)%2
                step = stairs - 1
        if(current_x == length):
            break
        list_modified(list,current_x, current_y, 0)
    return list   

def zigzag_encrypt(List, plain):
    number = 0
    for i in range(len(List[0])):
        for j in range(len(List)):
            if(List[j][i] != None):
                List[j][i] = number
                number += 1
    cipher = ''
    for i in range(len(List)):
        for j in range(len(List[0])):
            if(List[i][j] != None):
                List[i][j] = plain[List[i][j]]
                cipher = cipher + List[i][j]
    return cipher

def zigzag_decrypt(List, cipher):
    number = 0
    for i in range(len(List)):
        for j in range(len(List[0])):
            if(List[i][j] != None):
                List[i][j] = number
                number += 1
    plain = ''
    for i in range(len(List[0])):
        for j in range(len(List)):
            if(List[j][i] != None):
                List[j][i] = cipher[List[j][i]]
                plain = plain + List[j][i]
    return plain

cipher = 'pi arkirmndcnlaesihceomgnray   lwhvga,aytssall  ar pilsh'
plain = 'programming, and cryptanalysis are all skills which have'
quiz = 'algs ae ralin esact xeteuyseoranuileso s edtv  doariud eenc'

for i in range(3,20):
    zigzag = zigzag_build(len(cipher),i)
    if(zigzag_decrypt(zigzag, cipher) == plain):
        stairs = i
        break
zigzag = zigzag_build(len(quiz), stairs)
print(zigzag_decrypt(zigzag,quiz))