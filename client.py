import socket
from constants import HOST, PORT

# Setting up client connection
client_socket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM)
# Connection client to server
client_socket.connect((HOST, PORT))
#
complete_msg = ''
while True:
    msg = client_socket.recv(1024)
    if len(msg) <= 0:
        break
    else:
        complete_msg += msg.decode('utf-8')
print(complete_msg)