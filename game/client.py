import socket

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    print("Connected to the server.")

    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        print(message)

        # Check if the message is a prompt (ends with a colon)
        if message.strip().endswith('?'):
            response = input(":")  # Take input from the user
            client_socket.sendall(response.encode())  # Send the response back to the server

    client_socket.close()

if __name__ == "__main__":
    main()
