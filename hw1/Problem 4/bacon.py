lookup = {'A':'aaaaa', 'B':'aaaab', 'C':'aaaba', 'D':'aaabb', 'E':'aabaa', 
        'F':'aabab', 'G':'aabba', 'H':'aabbb', 'I':'abaaa', 'J':'abaab', 
        'K':'ababa', 'L':'ababb', 'M':'abbaa', 'N':'abbab', 'O':'abbba', 
        'P':'abbbb', 'Q':'baaaa', 'R':'baaab', 'S':'baaba', 'T':'baabb', 
        'U':'babaa', 'V':'babab', 'W':'babba', 'X':'babbb', 'Y':'bbaaa', 'Z':'bbaab'}    

def bacon_encrypt(cipher_text):
    cipher = ''
    for char in cipher_text:
        if(char.isalpha()):
            cipher += char
    cipher = cipher.strip()
    bacon = ""
    for i in range(len(cipher)):
        if(i%5==0):
            bacon = bacon + " "
        if(cipher[i].islower()):
            bacon = bacon + 'a'
        elif(cipher[i].isupper()):
            bacon = bacon + 'b'
        else:
            pass
    bacon = bacon.strip(' ')
    bacon = bacon.split(' ')
    result = ""
    for i in range(len(bacon)):
        for j in range(len(lookup)):
            if(bacon[i]==list(lookup.values())[j]):
                result = result + list(lookup.keys())[j]
    return result.rstrip('A')

#error = "are all SkILlS wHICh hAve BeEn rEquirEd BY pRiOR Ctf CoNtESts aT DEf Con. therE are TWO maIN Styles Of CaPtuRe the flAg cOmpetItioNS: aT the flag competitions: attack/defense and jeopardy!."
#print(bacon_encrypt(error))