import socket

CHUNK_SIZE = 1024

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
