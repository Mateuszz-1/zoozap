import socket
import msgpack
import struct
import random

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 12345))

    print("Connected to the server.")
    options = []

    while True:
        message_type, message = receive_message(client_socket)

        if not message:
            # Stop if no data is received
            break

        if message_type == b'T':  # Text message
            print("(T) Received: ", message.decode())
            message = message.decode() # Decode the message from bytes to string
            # Check if the message is a prompt
            if message.strip().endswith('?'):
                response = str(random.choice(options)) if options else print("No options available") # Pick a random option
                client_socket.sendall(response.encode())  # Send the response back to the server
                print("Response Sent:", response)
        elif message_type == b'M':  # MessagePack message
            data = msgpack.unpackb(message, raw=False) # Unpack the messagepack data
            print("(M) Received: ", data)
            options = data
        else:
            print("Unknown Message Received:")
            print(message)
            print("-UNKNOWN END")

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
