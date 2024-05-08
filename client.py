import socket
import json

def send_message(client_socket, message):
    client_socket.send(json.dumps(message).encode('utf-8'))

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
