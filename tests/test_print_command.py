# unit test to test the function of print to screen and file

import unittest
from unittest.mock import Mock
import argparse
from cryptography.fernet import Fernet
import sys
import os
import io

# Add the 'source' directory to the sys.path
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../source')))

# Import the functions from server.py
from server import receive_message, receive_file

class TestServer(unittest.TestCase):
    def setUp(self):
        self.client_socket = Mock()
        self.args = argparse.Namespace(
            print_to_screen=False, print_to_file=False)
        self.key = Fernet.generate_key()
        self.fernet = Fernet(self.key)

    def test_receive_message_print_to_screen(self):
        self.client_socket.recv.return_value = b'{"message": "Hi, group B!"}'
        self.args.print_to_screen = True
        self.args.print_to_file = False
        # Redirect stdout to a buffer
        stdout = sys.stdout
        sys.stdout = io.StringIO()
        result = receive_message(self.client_socket, self.args)
        # Get the console output
        output = sys.stdout.getvalue()
        # Restore stdout
        sys.stdout = stdout
        self.assertEqual(result, {'message': 'Hi, group B!'})
        self.assertEqual(
            output.strip(), "Received message: {'message': 'Hi, group B!'}")

    def test_receive_file_print_to_file(self):
        # Generate a valid encrypted token
        encrypted_data = self.fernet.encrypt(b'test file data')
        self.client_socket.recv.return_value = encrypted_data
        self.args.print_to_screen = False
        self.args.print_to_file = True
        result = receive_file(self.client_socket,
                              'groupb.txt', self.fernet, self.args)
        self.assertEqual(result, "Received and decrypted file: groupb.txt")
        # Check the contents of the file
        with open('groupb.txt', 'r') as f:
            file_contents = f.read()
        self.assertIn("Received and decrypted file: groupb.txt", file_contents)


if __name__ == '__main__':
    unittest.main()

