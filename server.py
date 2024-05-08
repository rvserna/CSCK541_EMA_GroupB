import socket
import json
import threading

CHUNK_SIZE = 1024

def receive_message(client_socket):
    data = client_socket.recv(CHUNK_SIZE).decode('utf-8')
    if not data:
        return {}
    print("recieve message data", data)
    return json.loads(data)


def receive_file(client_socket, file_name):
    with open(f"received_file_{file_name}", 'wb') as file:
        file_data = client_socket.recv(CHUNK_SIZE)
        file.write(file_data)

def handle_client(client_socket,server_socket):
    while True:
        message = receive_message(client_socket)
        if 'message' in message:
       
            if message['message'].lower() == 'exit':
                client_socket.send("exit".encode("utf-8"))
                break
    
        if 'file' in message and message['file']:
                file_name = message['file_name']
                receive_file(client_socket, file_name)
     
    client_socket.close()
    print("Connection to client closed")
    # close server socket
    server_socket.close()
    

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    server_socket.bind((host, port))
    server_socket.listen(0)

    print(f"Listening on {host}:{port}")

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address[0]}:{client_address[1]}")
        
        except Exception as e:
            break


if __name__ == "__main__":
    run_server()
