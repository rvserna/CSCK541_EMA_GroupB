import socket

CHUNK_SIZE = 1024

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    server_socket.bind((host, port))
    server_socket.listen(0)

    print(f"Listening on {host}:{port}")

if __name__ == "__main__":
    run_server()
