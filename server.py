import socket
import threading

HOST = "127.0.0.1" #loopback
SERVER_PORT = 60888
FORMAT = "utf8"

clients = []

def traoDoi(connection, address):
    print('Client information:')
    print('Server: ', address)
    print('Connect: ', connection.getsockname())

    while True:
        try:
            msg = connection.recv(2014).decode(FORMAT)
            if not msg:
                break
            print('Message: {}'.format(msg))
            print('Tin nhan duoc gui tu: {}'.format(address))
            danhSach(msg, connection)
        except:
            break

    connection.close()
    clients.remove(connection)


def danhSach(msg, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(msg.encode(FORMAT))
            except:
                client.close()
                clients.remove(client)



def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #sock stream de dung tcp

    s.bind((HOST, SERVER_PORT))
    s.listen()

    print('Server information:')
    print('Server: {}\nPort: {}'.format(HOST, SERVER_PORT))
    print('Loading...')

    #ket noi nhieu Client cung luc
    nClient = 0
    while(nClient < 3):
        try:
            connection, address = s.accept()
            clients.append(connection)
            thr = threading.Thread(target= traoDoi, args= (connection, address))
            thr.daemon = False
            thr.start()
        except:
            print('404')

        nClient += 1

    s.close()

if __name__ == "__main__":
    main()

