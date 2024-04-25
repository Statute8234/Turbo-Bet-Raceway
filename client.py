import socket

def start_client(server_host, server_port, closed = False):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        print("Connected to the server")
        
        while True:
            message = input("Enter message (type 'quit' to disconnect): ")
            if message.lower() == 'quit':
                break
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024)
            print(f"Server response: {response.decode('utf-8')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if closed:
            client_socket.close()
            print("Disconnected from the server")
        
    # Reconnection logic
    while True:
        action = input("Do you want to reconnect? (yes/no): ").lower()
        if action == 'yes':
            start_client(server_host, server_port)
        elif action == 'no':
            break

if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432
    start_client(HOST, PORT)
