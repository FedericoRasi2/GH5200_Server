import PySimpleGUI as sg
import socket
import threading

# Funzione per gestire la connessione in entrata
def handle_connection(client_socket):
    try:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            # Visualizza i dati ricevuti sulla finestra grafica
            window.write_event_value('-UPDATE-', f'Dati ricevuti: {data.decode()}')
    except Exception as e:
        # Gestisci eventuali errori
        window.write_event_value('-UPDATE-', f'Errore durante la ricezione dei dati: {str(e)}')
    finally:
        client_socket.close()

# Funzione per avviare il server
def start_server(listen_ip, listen_port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((listen_ip, listen_port))
    server_socket.listen(5)
    window.write_event_value('-UPDATE-', 'In attesa di connessioni...')
    while True:
        client_socket, addr = server_socket.accept()
        # Visualizza lo stato della connessione sulla finestra grafica
        window.write_event_value('-UPDATE-', f'Connesso da: {addr[0]}:{addr[1]}')
        # Avvia il thread per gestire la connessione
        connection_thread = threading.Thread(target=handle_connection, args=(client_socket,))
        connection_thread.start()

# Funzione per avviare il server in un thread separato
def start_server_thread():
    listen_ip = values['-IP-']
    listen_port = int(values['-PORT-'])
    start_server(listen_ip, listen_port)

# Definisci il layout della finestra
layout = [
    [sg.Text('Indirizzo IP del server:'), sg.InputText(key='-IP-')],
    [sg.Text('Porta:'), sg.InputText(key='-PORT-')],
    [sg.Button('Avvia il server'), sg.Button('Esci')],
    [sg.Text('', size=(40, 1), key='-STATUS-')],
    [sg.Multiline('', size=(40, 10), key='-LOG-', autoscroll=True)],
]

# Crea la finestra
window = sg.Window('Server Socket', layout, finalize=True)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Esci':
        break
    elif event == 'Avvia il server':
        # Avvia il server in un thread separato per evitare il blocco
        server_thread = threading.Thread(target=start_server_thread)
        server_thread.start()
    elif event == '-UPDATE-':
        # Aggiorna il log con lo stato dell'operazione
        log_text = values['-LOG-']
        log_text += f'{values["-UPDATE-"]}\n'
        window['-LOG-'].update(log_text)

window.close()
