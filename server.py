Code made by XZ100000
Github:
https://github.com/XZ100000/






import socket
import threading
import logging
from cryptography.fernet import Fernet
import datetime

# Set up logging
logging.basicConfig(filename=f'data/{datetime.date.today()}.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

print("The code is now running...")

# Permanent encryption key
KEY = "6oAd9OxSvVQfI5Ouy0ZuqX18c2W6xHzO4oyV8wA3S4U=" # Make your random key
cipher = Fernet(KEY.encode())

# Server's IP and port
HOST = '0.0.0.0'
PORT = 1234 # Enter a port that is allowed tru your wifi router

# List of connected clients and their usernames
clients = []
usernames = {}

def broadcast(message, sender_socket):
    """Send messages to all connected clients except the sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                # Remove the client if sending fails
                client.close()
                clients.remove(client)

def handle_client(client_socket):
    """Handle communication with a single client."""
    try:
        # Receive username
        encrypted_username = client_socket.recv(1024)
        username = cipher.decrypt(encrypted_username).decode('utf-8')
        usernames[client_socket] = username
        welcome_message = f"{username} has connected."
        logging.info(welcome_message)
        broadcast(cipher.encrypt(welcome_message.encode('utf-8')), client_socket)

        while True:
            message = client_socket.recv(1024)
            if not message:
                break
            decrypted_message = cipher.decrypt(message).decode('utf-8')
            broadcast_message = f"{usernames[client_socket]}: {decrypted_message}"
            logging.info(broadcast_message)
            broadcast(cipher.encrypt(broadcast_message.encode('utf-8')), client_socket)
    except:
        pass
    finally:
        client_socket.close()
        clients.remove(client_socket)
        leave_message = f"{usernames[client_socket]} has disconnected."
        logging.info(leave_message)
        broadcast(cipher.encrypt(leave_message.encode('utf-8')), client_socket)
        del usernames[client_socket]

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"Server is listening on {HOST}:{PORT}")
    print(f"Encryption key: {KEY}")

    while True:
        client_socket, client_address = server.accept()
        print(f"Connected to {client_address}")

        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
