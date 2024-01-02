import sqlite3
import os
from werkzeug.security import check_password_hash

class DatabaseHandler:
    def __init__(self, database_name: str):
        self.database_path = database_name
        self.conn = None
        self.connect_to_db()

    def connect_to_db(self):
        try:
            self.conn = sqlite3.connect(self.database_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            print(f"Erreur de connexion à la base de données: {e}")
        

    def create_utilisateur(self, utilisateur: str, motDePasse: str, email: str):
        try:
            with self.conn:
                query = "INSERT INTO utilisateurs (nomUtilsateur, motDePasse, email) VALUES (?, ?, ?);"
                self.conn.execute(query, (utilisateur, motDePasse, email))
            return True
        except sqlite3.Error as e:
            print(f"Erreur lors de la création de l'utilisateur: {e}")
            return False

    def connect_utilisateur(self, utilisateur: str, motDePasse: str):
        try: 
            query = "SELECT * FROM utilisateurs WHERE nomUtilsateur = ?;"
            cursor = self.conn.cursor()
            cursor.execute(query, (utilisateur,))
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user['motDePasse'], motDePasse):
                return True
            return False
        except sqlite3.Error as e:
            print(f"Erreur lors de la connexion de l'utilisateur: {e}")
            return False

    def __del__(self):
        if self.conn:
            self.conn.close()
