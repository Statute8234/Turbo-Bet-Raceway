import socket
import pickle
import threading

# Server configuration
SERVER = "localhost"
PORT = 5555

# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

server.listen()
print(f"Server is listening on {SERVER}:{PORT}")

# Store connected clients
clients = []

def handle_client(conn, addr):
    print(f"New connection from {addr}")
    connected = True
    while connected:
        try:
            # Receive data from client
            data = conn.recv(2048)
            if not data:
                break

            # Broadcast received data to all other clients
            for client in clients:
                if client != conn:
                    client.send(data)
        except:
            connected = False

    print(f"Connection from {addr} closed")
    clients.remove(conn)
    conn.close()

def accept_connections():
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"Active connections: {threading.active_count() - 1}")

# Start accepting connections
accept_connections()