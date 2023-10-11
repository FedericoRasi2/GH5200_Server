import socket

# Configura l'indirizzo IP e la porta del tuo server
HOST = '0.0.0.0'  # Puoi utilizzare '0.0.0.0' per ascoltare su tutte le interfacce di rete
PORT = 12345  # Sostituisci con la porta desiderata

# Byte di risposta per accettare i dati
response_byte = b'\x01'  # Cambia il byte di risposta se necessario

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"In ascolto su {HOST}:{PORT}")
    
    # Accetta le connessioni in entrata
    conn, addr = server_socket.accept()
    with conn:
        print(f"Connesso a {addr}")
        
        # Ricevi i dati dal tracker
        data = conn.recv(1024)  # Modifica la dimensione del buffer se necessario
        if not data:
            print("Nessun dato ricevuto")
        else:
            print(f"Dati ricevuti: {data}")
            # Invia il byte di risposta
            conn.sendall(response_byte)
            print("Byte di risposta inviato")
