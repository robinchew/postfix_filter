import socket

MILTER_ADDRESS = '0.0.0.0'
MILTER_PORT = 8888

def handle_client(client_socket):
    data = b''

    while True:
        chunk = client_socket.recv(4096)
        if chunk == b'quit\r\n':
            break
        data += chunk

    # Print the received email
    print(data.decode('utf-8',errors='ignore'))

if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((MILTER_ADDRESS, MILTER_PORT))
    server.listen(5)

    print(f"Listening on {MILTER_ADDRESS}:{MILTER_PORT}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr[0]}:{addr[1]}")
        handle_client(client_socket)
        client_socket.close()