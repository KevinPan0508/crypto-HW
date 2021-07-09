import socks
import socket
import socks                      
from urllib.parse import urlparse       
from pwn import *     
import hashlib
import binascii
import base64

hostname = 'http://cnsggnhxxfujmdtqp4hddfd3xp2rjclz7yfiuguekdcvwar7f72yrtad.onion'
onion_address = 'cnshwdnxwnxb2mosesf2uzyvuj34ykxhmy452k6ox4t5n67563rzgmad.onion'


#connect server
SOCKS_HOST = 'localhost'                                             
SOCKS_PORT = 9050                                                    
SOCKS_TYPE = socks.PROXY_TYPE_SOCKS5                              
parsed = urlparse(hostname)
socket = socks.socksocket()                                          
socket.setproxy(SOCKS_TYPE, SOCKS_HOST, SOCKS_PORT)   
socket.connect((parsed.netloc, 3002)) 
r = remote.fromsocket(socket)
txt = r.recvuntil(b'address: ').decode()
print(txt)
r.sendline(onion_address)
r.interactive()

