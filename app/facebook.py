from flask import Flask, redirect, request, session, jsonify
from requests_oauthlib import OAuth2Session
from requests_oauthlib.compliance_fixes import facebook_compliance_fix
import requests
from app import app

# Facebook OAuth configuration
CLIENT_ID = '687317540258045'
CLIENT_SECRET = 'ec6e8f1c07710a41162de17ed1851a3d'
# REDIRECT_URI = 'http://localhost:5000/callback'  # Set this to your callback URL
REDIRECT_URI = 'https://test-auth-i2mu.onrender.com/fb/callback'  # Set this to your callback URL

# Facebook OAuth endpoints
AUTHORIZATION_BASE_URL = 'https://www.facebook.com/v11.0/dialog/oauth'
TOKEN_URL = 'https://graph.facebook.com/v11.0/oauth/access_token'


@app.route('/login/fb')
def fb_login():
    facebook = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    facebook = facebook_compliance_fix(facebook)
    authorization_url, state = facebook.authorization_url(AUTHORIZATION_BASE_URL)

    # Save the state to compare it in the callback
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route('/fb/callback')
def fb_callback():
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
        # return f"User ID: {user_data['id']}, Name: {user_data['name']}, Email: {user_data.get('email', 'N/A')}"
        return jsonify(user_data), 200
    else:
        return 'Failed to fetch user data from Facebook Graph API'
