import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print('Message from server: {}'.format(message))
        except Exception as e:
            print('\nError: ', e)
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 9999))
    print('Connected to server by: ', client.getsockname())
    threading.Thread(target=receive_messages, args=(client,)).start()

    while True:
        message = input()
        client.sendall(message.encode('utf-8'))
    


if __name__ == "__main__":
    main()
