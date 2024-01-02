import socket
import threading
import json

# Paramètres de configuration du client
HOST = '127.0.0.1'
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                print(f"Message reçu: {message}")
            else:
                print("Aucun message reçu du serveur.")
                break
        except Exception as e:
            print(f"Erreur lors de la réception du message: {e}")
            break

def send_data_to_server(action, username, password, email=None):
    try:
        client.sendall(action.encode())
        client.sendall(username.encode())
        client.sendall(password.encode())

        if email:
            client.sendall(email.encode())
    except Exception as e:
        print(f"Erreur lors de l'envoi des données au serveur: {e}")

def handle_connection(client):
    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    while True:
        action = input("Voulez-vous vous connecter ou vous enregistrer ? Tapez 'connecter' ou 'enregistrer' : ")
        if action in ['connecter', 'enregistrer']:
            username = input("Entrez votre nom d'utilisateur : ")
            password = input("Entrez votre mot de passe : ")
            email = input("Entrez votre email : ") if action == 'enregistrer' else None

            send_data_to_server(action, username, password, email)
            break
        else:
            print("Commande non reconnue. Veuillez taper 'connecter' ou 'enregistrer'.")

try:
    client.connect((HOST, PORT))
    print("Connexion avec succès au serveur.")
    handle_connection(client)
except Exception as e:
    print(f"Echec de la connexion au serveur {HOST} {PORT}. Erreur: {e}")
    exit()
