import ed25519
import hashlib
import base64
import threading

def search(string):
    version = b'\x03'
    while True:
        priv_key, pub_key = ed25519.create_keypair()
        pub_key_byte = pub_key.to_bytes()
        priv_key_byte = priv_key.to_bytes()
        hash_byte = b'.onion checksum' + pub_key_byte + version
        sha3 = hashlib.sha3_256()
        sha3.update(hash_byte)
        checksum = sha3.digest()[:2]
        onion = base64.b32encode(pub_key_byte + checksum + version).decode().lower()
        if(onion[:len(string)] == string):
            print(onion + '.onion')
            print(pub_key_byte)
            print(priv_key_byte)


def multi_search(num, string):
    t_list = []
    for i in range(num):
        t_list.append(threading.Thread(target=search, args=(string,)))
        t_list[i].start()

multi_search(4, 'cnshw')