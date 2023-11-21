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

        if b'mail from:' in data.lower():
            sender_address = data.decode('utf-8').split('mail from:')[1].split('\r\n')[0].strip()

            # Extract the domain from the sender address
            sender_domain = sender_address.split('@')[1]

            # Check if the sender domain is on the rejection list
            if sender_domain == 'example.com':
                print(f"Rejecting email from {sender_address}")

                # SMTP Error Messages
                # https://support.google.com/a/answer/3726730?sjid=12069780384646155174-AP
                client_socket.sendall(b'550 5.7.1 Sender rejected\r\n')  # SMTP rejection response
                break

            print(f"Accepting email from {sender_address}")

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
