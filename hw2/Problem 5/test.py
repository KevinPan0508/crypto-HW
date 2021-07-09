import socks
import socket
import socketio
from urllib.parse import urlparse 
sio = socketio.Client()

sio.connect('http://localhost:80')
sio.emit('connected')
sio.recvline()