from flask import Flask, request, jsonify
import requests
import os
import json
import time
from datetime import datetime

app = Flask(__name__)

# Configuration
DISCORD_CLIENT_ID = "1482471026448142486"
DISCORD_CLIENT_SECRET = "NBazmlKbXjQGy3S4-USFUw8d_3Iez647"
REDIRECT_URI = 'https://ton-app.vercel.app/callback'

# Chemin du fichier JSON (dans /tmp car Vercel est en lecture seule)
DATA_FILE = '/tmp/users.json'

def load_users():
    """Charge les utilisateurs depuis le fichier JSON"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
    except:
        pass
    return {}

def save_users(users):
    """Sauvegarde les utilisateurs dans le fichier JSON"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(users, f, indent=2)
    except:
        pass

def handler(request):
    """Callback OAuth2"""
    
    # Récupérer le code
    code = request.args.get('code')
    
    if not code:
        return jsonify({"error": "Code non reçu"}), 400
    
    # Échanger le code contre des tokens
    data = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    response = requests.post('https://discord.com/api/oauth2/token', data=data, headers=headers)
    
    if response.status_code != 200:
        return jsonify({"error": "Erreur d'authentification"}), 400
    
    token_data = response.json()
    
    # Récupérer les infos utilisateur
    user_info = requests.get('https://discord.com/api/users/@me', headers={
        'Authorization': f'Bearer {token_data["access_token"]}'
    }).json()
    
    # Sauvegarder dans le fichier JSON
    users = load_users()
    users[user_info['id']] = {
        'user_id': user_info['id'],
        'username': f"{user_info['username']}#{user_info['discriminator']}",
        'avatar': user_info.get('avatar', ''),
        'access_token': token_data['access_token'],
        'refresh_token': token_data['refresh_token'],
        'expires_at': int(time.time()) + token_data['expires_in'],
        'created_at': datetime.now().isoformat()
    }
    save_users(users)
    
    # Page HTML de succès
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Authentification réussie</title>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .card {{
                background: white;
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                text-align: center;
                max-width: 400px;
            }}
            .success {{
                width: 80px;
                height: 80px;
                background: #4CAF50;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin: 0 auto 20px;
                font-size: 40px;
                color: white;
            }}
            h1 {{ color: #333; }}
            .user {{ 
                background: #f5f5f5;
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                font-weight: bold;
            }}
            button {{
                background: #4CAF50;
                color: white;
                border: none;
                padding: 12px 30px;
                border-radius: 5px;
                font-size: 16px;
                cursor: pointer;
            }}
            button:hover {{ background: #45a049; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="success">✓</div>
            <h1>Authentification réussie !</h1>
            <div class="user">{users[user_info['id']]['username']}</div>
            <p>Tu peux maintenant retourner sur Discord.</p>
            <p>Le bot va pouvoir t'ajouter aux serveurs.</p>
            <button onclick="window.close()">Fermer</button>
        </div>
    </body>
    </html>
    """
    
    return html, 200, {'Content-Type': 'text/html'}
