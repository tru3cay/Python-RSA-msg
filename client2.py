import socket
import threading

HOST = "127.0.0.1" #loopback
SERVER_PORT = 60888
FORMAT = "utf8"

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode(FORMAT)
            if not message:
                break
            print(message)
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    threading.Thread(target=receive_messages, args=(client,)).start()
    try:
        print('Client windows')
        client.connect((HOST, SERVER_PORT))
        print('Server: ', client.getsockname())

        while True:
            msg = input('Message: ')
            client.sendall(msg.encode(FORMAT))

            #msg = client.recv(1024).decode(FORMAT)
            #print('Server respond: {}'.format(msg))

    except:
        print('404')
        
    client.close()


if __name__ == "__main__":
    main()
