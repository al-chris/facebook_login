from flask import Flask, render_template, request, session, jsonify
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Facebook OAuth configuration
CLIENT_ID = '687317540258045'
CLIENT_SECRET = 'ec6e8f1c07710a41162de17ed1851a3d'
# REDIRECT_URI = 'http://localhost:5000/callback'  # Set this to your callback URL
REDIRECT_URI = 'https://test-auth-i2mu.onrender.com/callback'  # Set this to your callback URL

# Facebook OAuth endpoints
AUTHORIZATION_BASE_URL = 'https://www.facebook.com/v11.0/dialog/oauth'
TOKEN_URL = 'https://graph.facebook.com/v11.0/oauth/access_token'

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/terms_of_service')
def t_o_s():
    return render_template("terms_of_service.html")

@app.route('/privacy_policy')
def privacy():
    return render_template("privacy_policy")

from app import facebook, tiktok, google