
import sys

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
def caesar_decrypt(text,s): 
    result = ''
    for i in range(len(text)):
        if(text[i].islower()):
            for j in range(len(alphabet.lower())):
                if(text[i]==alphabet.lower()[j]):
                    result = result + alphabet.lower()[(j+s)%26]
        elif(text[i].isupper()):
            for j in range(len(alphabet)):
                if(text[i]==alphabet[j]):
                    result = result + alphabet[(j+s)%26]
        else:
            result = result + text[i]
    return result

cipher = 'bmm tljmmt xijdi ibwf cffo sfrvjsfe cz qsjps DUG dpouftut bu'

list = []
for i in range(1,27):
    plain_text = caesar_decrypt(cipher,i)
    list.append(plain_text)
    print('index = {0}, string = {1}'.format(i-1,plain_text))





