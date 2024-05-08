import socket

def run_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8000
    client_socket.connect((host, port))

    print(f"Client connected to server socket")


if __name__ == "__main__":
    run_client()
