import socket
import threading

clients = {}
public_keys = {}

def handle_client(client_socket, addr):
    # Nhận định danh và khóa công khai từ client
    data = client_socket.recv(4096)
    identifier, public_key_data = data.split(b'|', 1)
    identifier = identifier.decode('utf-8')
    public_keys[identifier] = public_key_data
    clients[identifier] = client_socket

    # Hiển thị khóa công khai của client mới kết nối
    print(f"Client {identifier} connected with public key:\n{public_key_data.decode('utf-8')}\n")

    # Gửi định danh và khóa công khai của client mới cho tất cả các client khác
    for other_identifier, client in clients.items():
        if other_identifier != identifier:
            client.send(f"{identifier}|".encode('utf-8') + public_key_data)
            client_socket.send(f"{other_identifier}|".encode('utf-8') + public_keys[other_identifier])

    while True:
        try:
            encrypted_message = client_socket.recv(4096)
            if not encrypted_message:
                break
            print(f"Received from {identifier}")
            broadcast(encrypted_message, client_socket)
        except Exception as e:
            print(f"Error: {e}")
            break
    client_socket.close()
    del clients[identifier]
    del public_keys[identifier]
    print(f"Connection with {identifier} closed")

def broadcast(message, sender_socket):
    for client in clients.values():
        if client != sender_socket:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error: {e}")
                client.close()
                for identifier, sock in clients.items():
                    if sock == client:
                        del clients[identifier]
                        break

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server started and listening on port 9999")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()

if __name__ == "__main__":
    main()
