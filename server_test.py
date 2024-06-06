import socket
import threading

clients = []

# Hàm xử lý kết nối của client
def handleClient(client_socket, addr):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print('\nMessage from {}: {}'.format(addr, message))
            broadCast(message, client_socket)

        except Exception as e:
            print('\nError: ', e)
            break

    client_socket.close()
    clients.remove(client_socket)
    print('\n{} closed'.format(addr))

# Hamf gửi tin nhắn tới tất cả các client có trong clients
def broadCast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                print('Message send to {}'.format(client.getpeername()))
                client.sendall(message.encode('utf-8'))

            except Exception as e:
                print('\nError: ', e)
                client.close()
                clients.remove(client)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9999))
    server.listen(5)
    print('Loading...')

    nClient = 0
    while nClient < 2:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        print('\nAccepted connection from {}'.format(addr))
        client_handler = threading.Thread(target=handleClient, args=(client_socket, addr))
        client_handler.start()
        nClient += 1

if __name__ == "__main__":
    main()
