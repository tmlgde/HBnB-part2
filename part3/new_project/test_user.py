#!/usr/bin/python3
import requests

# 🔧 Adresse locale de l'API
url = "http://127.0.0.1:5000/api/v1/auth/login"

# 📧 Données de connexion de test (utilisateur déjà créé)
payload = {
    "email": "john.doe@example.com",
    "password": "monmotdepasse"
}

# 🔐 Requête POST
response = requests.post(url, json=payload)

# 📤 Affichage du résultat
print("Status Code:", response.status_code)
print("Réponse JSON:", response.json())
