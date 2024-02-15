import socket
import json
import random

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    print("Connected to the server.")

    while True:
        message = client_socket.recv(1024).decode()
        print(message)
        if not message:
            break
        try:
            message = json.loads(message)
        except:
            print(message)

        if isinstance(message, list):
            options = message
        elif isinstance(message, dict):
            options = list(message.keys())
        else:
            # Check if the message is a prompt (ends with a colon)
            if message.strip().endswith('?'):
                response = random(options)  # Pick a random option
                client_socket.sendall(response.encode())  # Send the response back to the server

    client_socket.close()

if __name__ == "__main__":
    main()
