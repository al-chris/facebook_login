from flask import Flask, redirect, url_for, request, session
from requests_oauthlib import OAuth2Session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Facebook OAuth configuration
CLIENT_ID = '687317540258045'
CLIENT_SECRET = 'ec6e8f1c07710a41162de17ed1851a3d'
# REDIRECT_URI = 'http://localhost:5000/callback'  # Set this to your callback URL
REDIRECT_URI = 'https://facebook-login-v03a.onrender.com/callback'  # Set this to your callback URL

# Facebook OAuth endpoints
AUTHORIZATION_BASE_URL = 'https://www.facebook.com/v11.0/dialog/oauth'
TOKEN_URL = 'https://graph.facebook.com/v11.0/oauth/access_token'

@app.route('/')
def index():
    return '<a href="/login">Login with Facebook</a>'

@app.route('/login')
def login():
    facebook = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    authorization_url, state = facebook.authorization_url(AUTHORIZATION_BASE_URL)

    # Save the state to compare it in the callback
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # Check for CSRF attacks
    # if request.args.get('state') != session.pop('oauth_state', None):
    #     print('here')
    #     return 'Invalid state'

    facebook = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = facebook.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)


    # Use the token to make a request to the Facebook Graph API to get user data
    graph_api_url = 'https://graph.facebook.com/me'
    params = {'access_token': token['access_token'], 'fields': 'id,name,email'}
    response = requests.get(graph_api_url, params=params)

    if response.status_code == 200:
        user_data = response.json()
        # Return the user's data (you can customize this response as needed)
        return f"User ID: {user_data['id']}, Name: {user_data['name']}, Email: {user_data.get('email', 'N/A')}"
    else:
        return 'Failed to fetch user data from Facebook Graph API'

    # You can now use the token to access the user's data
    # For example, you can get the user's profile using the Facebook Graph API
    # For demonstration purposes, let's just return the token
    print(token)
    return f'Token: {token}'

