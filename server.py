"""
Server script for receiving files and messages from clients.
"""
import socket
import json
import threading
import argparse
from cryptography.fernet import Fernet

CHUNK_SIZE = 1024

# add argparse for commend-line options 
parser = argparse.ArgumentParser(description = 'Configure print setting.')
parser.add_argument('--print-to-screen', action = 'store_true', help = 'Print received items to the screen')
parser.add_argument('--print-to-file', action='store_true', help='Print received items to a file')
args = parser.parse_args()

def receive_message(client_socket):
    """
    Receive message from the client.
    Arguments:
        client_socket (socket.socket)
    Returns:
        dictionary: Received message as a dictionary.
    """
    data = client_socket.recv(CHUNK_SIZE).decode('utf-8')
    if not data:
        return {}
    #print("recieve message data", data)
    #return json.loads(data)

    # modify to suit the logic of print received items
    message = json.loads(data)
    if args.print_to_screen:
        print("Received message:", message)
    if args.print_to_file:
        with open('groupb.txt', 'a') as f:
            f.write("Received message: " + str(message) + "\n")
    return message


def receive_file(client_socket, file_name, f):
    """
    Receive a file from the client.
    Arguments:
        client_socket (socket.socket).
        file_name (string):file to receive.
        f (cryptography.fernet.Fernet): Fernet encryption object.
    """

    with open(f"received_file_{file_name}", 'wb') as file:
        file_data = client_socket.recv(CHUNK_SIZE)
        # Decrypt file data before writing
        decrypted_data = f.decrypt(file_data)
        file.write(decrypted_data)
        # Proof of decryption during testing
        # print(f"Received and decrypted file: {file_name}")

        # modify to suit the logic of print received items
        if args.print_to_screen:
            print(f"Received and decrypted file: {file_name}")
        if args.print_to_file:
            with open('groupb.txt', 'a') as f:
                f.write(f"Received and decrypted file: {file_name}\n")


def handle_client(client_socket,server_socket, f):
    """
    Handle comms with a client.
    Argumentss:
        client_socket (socket.socket)
        server_socket (socket.socket)
        f (cryptography.fernet.Fernet): Fernet encryption object.
    """
    while True:
        message = receive_message(client_socket)
        if 'message' in message:
            if message['message'].lower() == 'exit':
                client_socket.send("exit".encode("utf-8"))
                break
        if 'file' in message and message['file']:
            file_name = message['file_name']
            receive_file(client_socket, file_name, f)
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server_socket.close()


def run_server():
    """
    Run the server to accept client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    server_socket.bind((host, port))
    server_socket.listen(0)

    print(f"Listening on {host}:{port}")

    # Generate or load the key
    try:
        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()
    except FileNotFoundError:
        print("Key file not found. Exiting.")
        return

    f = Fernet(key)

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

            client_id = "client_1"
            if client_id:
                client_thread = threading.Thread(target=handle_client, args=(
                    client_socket,server_socket, f))
                client_thread.start()
        except Exception as e:
            break


if __name__ == "__main__":
    run_server()
