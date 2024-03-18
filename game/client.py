import socket
import struct

def main():
    port = 50500
    while True:
        if port > 50600:
            print("No available ports")
            exit()
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect(('localhost', port))
            break
        except OSError as e:
                if e.errno == 61:
                    port += 1

    print(f"Connected to the server at port {port}.")

    while True:
        message_type, message = receive_message(client_socket)
        if not message:
            break

        if message_type == b'T':  # Text message
            print(message.decode())
            message = message.decode()
            # Check if the message is a prompt
            if message.strip().endswith('?'):
                # Take input from the user
                response = input(":")
                # Send the response back to the server
                client_socket.sendall(response.encode())

    client_socket.close()

def receive_message(client_socket):
    # Read the first byte to determine the message type
    message_type = client_socket.recv(1)
    if not message_type:
        # Connection closed
        return None

    # Read the next 4 bytes for the message length
    length_bytes = client_socket.recv(4)
    if len(length_bytes) < 4:
        raise ValueError("Received incomplete message length")
    
    # Unpack the message length
    message_length, = struct.unpack(">I", length_bytes)
    
    # Read the message data based on the length
    message_data = client_socket.recv(message_length)
    while len(message_data) < message_length:
        # Ensure the entire message is read
        more_data = client_socket.recv(message_length - len(message_data))
        if not more_data:
            raise ValueError("Received incomplete message")
        message_data += more_data
    
    return message_type, message_data

if __name__ == "__main__":
    main()
