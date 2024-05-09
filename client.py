"""
Client-side script for sending files and messages to a server.
"""
import socket
import json
import time
from cryptography.fernet import Fernet

TEXT_FILE = "data.txt"
PY_FILE = "dict.py"

# Define key file path
KEY_FILE = 'filekey.key'

def send_message(client_socket, message):
    """
    Send a message to the server.
    Aruments:
        client_socket (socket.socket)
        message (dictionary): Message to send as a dictionary.
    """
    client_socket.send(json.dumps(message).encode('utf-8'))

def send_file(client_socket, file_path, f):
    """
    Send an encrypted file to the server.
    Arguments:
        client_socket (socket.socket).
        file_path (string): Path of the file to send.
        f (cryptography.fernet.Fernet): Fernet encryption object.
    """
    try:
        with open(file_path, 'rb') as file:
            send_message(client_socket, {"file": True, "file_name": file_path.split(' ')[-1]})
            time.sleep(1)
            file_data = file.read()
             # Encrypt file_data before sending
            encrypted = f.encrypt(file_data)
            client_socket.send(encrypted)
            # proof of encryption during testing
            print(f"Sent encrypted file: {file_path}")
            print(f"with encrypted contents: {(encrypted)}")
    except FileNotFoundError:
        print("File not found")

def run_client():
    """
    run the client.
    """
     #Make or load the key in the existing file, filekey.key
    try:
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
    except FileNotFoundError:
        # make new key if it doesn't exist already
        key = Fernet.generate_key()
        with open('filekey.key', 'wb') as filekey:
            filekey.write(key)
    f = Fernet(key)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    client_socket.connect((host, port))

    print("Client connected to server socket")
    print(f"Sending {TEXT_FILE} file to server.")
    send_file(client_socket, TEXT_FILE, f)
    print(f"Sending {PY_FILE} file to server.")
    send_file(client_socket, PY_FILE, f)

    while True:
        message = input("Enter your message or type 'exit' to disconnect: ")

        message = {'message': message}
        send_message(client_socket, message)

        # receive message from the server
        response = client_socket.recv(1024)
        response = response.decode("utf-8")

        # if server sent us "exit" in the payload, we break out of the loop and close our socket
        if response.lower() == "exit":
            break
    client_socket.close()
    print("Connection to server closed")

if __name__ == "__main__":
    run_client()
