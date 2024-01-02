import socket
import threading
from flask import Flask, request, jsonify
import os
import sqlite3
from database_requetes import DatabaseHandler
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
database_projet = DatabaseHandler("database_projet.db")

# Paramètres de configuration du serveur
HOST = '127.0.0.1'
PORT = 5000
LISTENER_LIMIT = 5

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(LISTENER_LIMIT)
    print(f"Le serveur écoute sur {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"Connexion établie avec {address}")
        threading.Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    try:
        while True:
            response = client.recv(1024).decode('utf-8')
            if response:
                process_client_request(client, response)
            else:
                break
    except Exception as e:
        print(f"Erreur lors de la gestion du client: {e}")
    finally:
        client.close()

def process_client_request(client, response):
    if response == 'connecter':
        connect_client(client)
    elif response == 'enregistrer':
        register_client(client)
    else:
        client.send("Commande non reconnue.".encode('utf-8'))

def connect_client(client):
    try:
        username = client.recv(1024).decode('utf-8')
        password = client.recv(1024).decode('utf-8')

        if database_projet.connect_utilisateur(username, password):
            client.send("Connexion réussie !".encode('utf-8'))
        else:
            client.send("Échec de la connexion.".encode('utf-8'))
    except Exception as e:
        print(f"Erreur lors de la connexion du client: {e}")

def register_client(client):
    try:
        username = client.recv(1024).decode('utf-8')
        password = generate_password_hash(client.recv(1024).decode('utf-8'))
        email = client.recv(1024).decode('utf-8')

        if database_projet.create_utilisateur(username, password, email):
            client.send("Utilisateur créé avec succès.".encode('utf-8'))
        else:
            client.send("Échec de la création de l'utilisateur.".encode('utf-8'))
    except Exception as e:
        print(f"Erreur lors de l'enregistrement du client: {e}")

@app.route('/create_user', methods=['POST'])
def create_user():
    try:
        data = request.json
        username = data['username']
        password = generate_password_hash(data['password'])
        email = data['email']

        if database_projet.create_utilisateur(username, password, email):
            return jsonify({"message": "User created"}), 201
        else:
            return jsonify({"error": "Failed to create user"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(port=5000, debug=True, use_reloader=False)).start()
    start_server()
