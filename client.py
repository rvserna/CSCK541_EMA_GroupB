import socket
import json
import time

text_file = "data.txt"
py_file = "dict.py"

def send_message(client_socket, message):
    client_socket.send(json.dumps(message).encode('utf-8'))

def send_file(client_socket, file_path):
    try:
        with open(file_path, 'rb') as file:
            send_message(client_socket, {"file": True, "file_name": file_path.split(' ')[-1]})
            time.sleep(1)
            file_data = file.read()
            client_socket.send(file_data)
    except FileNotFoundError:
        print("File not found")

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    client_socket.connect((host, port))

    print(f"Client connected to server socket")

    while True:
        message = input("Enter your message or type 'exit' to disconnect: ")

        message = {'message': message}
        send_message(client_socket, message)



if __name__ == "__main__":
    run_client()
