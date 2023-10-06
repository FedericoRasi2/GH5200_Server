import socket
import threading

# Funzione per gestire la connessione in entrata
def handle_connection(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
    finally:
        client_socket.close()

# Funzione per avviare il server
def start_server(listen_ip, listen_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_ip, listen_port))
    server_socket.listen(5)
    while True:
        client_socket, addr = server_socket.accept()
        # Visualizza lo stato della connessione sulla finestra grafica
        # Avvia il thread per gestire la connessione
        connection_thread = threading.Thread(target=handle_connection, args=(client_socket,))
        connection_thread.start()

# Funzione per avviare il server in un thread separato
def start_server_thread():
    start_server("0.0.0.0", 56789)

server_thread = threading.Thread(target=start_server_thread)
server_thread.start()
