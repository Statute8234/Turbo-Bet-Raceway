import socket
import threading

def handle_client(client_socket, address):
    print(f"Connected to {address}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == '':
                break
            print(f"Received from {address}: {message}")
            # You can process the message here and send back a response
            client_socket.send("Message received".encode('utf-8'))
        except ConnectionResetError:
            break
        except Exception as e:
            print(f"Error with {address}: {e}")
            break
    client_socket.close()
    print(f"Connection closed with {address}")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, address = server_socket.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, address))
            thread.start()
            print(f"Active connections: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("Server is shutting down")
    finally:
        server_socket.close()

if __name__ == "__main__":
    HOST = '127.0.0.1'  # Localhost
    PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
    start_server(HOST, PORT)
