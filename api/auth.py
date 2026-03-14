from flask import Flask, redirect

app = Flask(__name__)

def handler(request):
    """Redirige vers l'authentification Discord"""
    
    # TES IDENTIFIANTS DIRECTEMENT ICI
    DISCORD_CLIENT_ID = "1482471026448142486"  # Remplace par ton vrai client ID
    REDIRECT_URI = "https://ton-app.vercel.app/callback"  # Remplace par ton URL Vercel
    
    auth_url = f"https://discord.com/api/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={REDIRECT_URI}&response_type=code&scope=identify%20guilds.join"
    
    return redirect(auth_url, 302)
