import unittest
import socket
import json

class TestClientServer(unittest.TestCase):
    def setUp(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(( '127.0.0.1', 8000))
    
    def tearDown(self):
        self.client_socket.close()
    
    def test_client_server(self):
        self.client_socket.send(json.dumps({'message': 'exit'}).encode('utf-8'))
        self.assertNotEqual(self.client_socket.recv(1024).decode(), {})
    

if __name__ == '__main__':
    unittest.main()