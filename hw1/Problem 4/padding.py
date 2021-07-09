import binascii


def padding_decrypt(cipher, key_byte, text):
    bin = binascii.hexlify(text)
    string = str(bin)[2:-1]
    result = ''
    for i in range(0,len(string),2):
        hex1 = int(string[i]+string[i+1],16)
        hex2 = int(key_byte[i]+key_byte[i+1],16)
        temp = str(hex(hex1^hex2)).replace('0x','')
        result = result + temp
    answer = binascii.unhexlify(bytes(result,encoding='utf-8'))
    return str(answer)[2:-1]
