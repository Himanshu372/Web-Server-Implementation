import socket
from constants import HOST, PORT

# Setting up server connection
listen_socket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM)
# Binding host and port for server
listen_socket.bind((HOST, PORT))
#
listen_socket.listen(5)
while True:
    client_socket, client_address = listen_socket.accept()
    print('Connection to {} established'.format(client_address))
    client_socket.send(bytes('Hi from Server-Client', 'utf-8'))
    client_socket.close()