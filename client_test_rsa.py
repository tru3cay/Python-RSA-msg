import socket
import threading
import rsa

# Tạo cặp khóa RSA
(public_key, private_key) = rsa.newkeys(2048)

# Lưu trữ khóa công khai của các client khác
public_keys = {}

def receive_messages(client_socket, private_key):
    while True:
        try:
            encrypted_message = client_socket.recv(4096)
            if not encrypted_message:
                break
            # Sử dụng khóa bí mật để giải mã tin nhắn
            message = rsa.decrypt(encrypted_message, private_key)
            print(f"Received from server: {message.decode('utf-8')}")
        except Exception as e:
            print(f"Error: {e}")
            break

def receive_public_keys(client_socket):
    while True:
        try:
            data = client_socket.recv(4096)
            if not data:
                break
            # Tách định danh và khóa công khai
            identifier, key_data = data.split(b'|', 1)
            public_keys[identifier.decode('utf-8')] = rsa.PublicKey.load_pkcs1(key_data)
            print(f"Received public key from {identifier.decode('utf-8')}")
        except Exception as e:
            print(f"Error receiving public key: {e}")
            break

def main():
    identifier = input("Enter your identifier (e.g., client1): ").encode('utf-8')

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))
    print("Connected to server")

    # Hiển thị khóa bí mật của client
    print(f"Your private key:\n{private_key.save_pkcs1().decode('utf-8')}\n")

    # Gửi định danh và khóa công khai tới server
    client.send(identifier + b'|' + public_key.save_pkcs1())

    threading.Thread(target=receive_public_keys, args=(client,)).start()
    threading.Thread(target=receive_messages, args=(client, private_key)).start()

    while True:
        message = input("").encode('utf-8')
        recipient_identifier = input("Enter recipient identifier: ").encode('utf-8')
        if recipient_identifier.decode('utf-8') in public_keys:
            recipient_key = public_keys[recipient_identifier.decode('utf-8')]
            # Sử dụng khóa công khai để mã hóa tin nhắn
            encrypted_message = rsa.encrypt(message, recipient_key)
            print(f"Encrypted message: {encrypted_message}")
            client.send(encrypted_message)
        else:
            print("Recipient public key not found")

if __name__ == "__main__":
    main()
