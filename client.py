import socket

HOST = "127.0.0.1" #loopback
SERVER_PORT = 60888
FORMAT = "utf8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    print('Client windows')
    client.connect((HOST, SERVER_PORT))
    print('Server: ', client.getsockname())

    msg = None
    while(msg != 'x'):
        msg = input('Message: ')
        client.sendall(msg.encode(FORMAT))

        #msg = client.recv(1024).decode(FORMAT)
        #print('Server respond: {}'.format(msg))

except:
    print('404')
    
client.close()
