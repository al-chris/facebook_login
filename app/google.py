from flask import Flask, redirect, request, session, jsonify
from requests_oauthlib import OAuth2Session
from app import app

# Google OAuth configuration
CLIENT_ID = ''
CLIENT_SECRET = ''
# REDIRECT_URI = 'http://localhost:5000/callback'  # Set this to your callback URL
REDIRECT_URI = 'https://test-auth-i2mu.onrender.com/google/callback'

# Google OAuth endpoints
AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'



@app.route('/login/google')
def google_login():
    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=['profile', 'email'])
    authorization_url, state = google.authorization_url(AUTHORIZATION_BASE_URL, access_type='offline')

    # Save the state to compare it in the callback
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route('/google/callback')
def google_callback():
    # Check for CSRF attacks
    # if request.args.get('state') != session.pop('oauth_state', None):
    #     return 'Invalid state'

    google = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = google.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)

    # Use the token to make a request to the Google API to get user data
    response = google.get(USER_INFO_URL)

    if response.status_code == 200:
        user_data = response.json()
        # Return the user's data (you can customize this response as needed)
        return jsonify(user_data), 200
    else:
        return 'Failed to fetch user data from Google API'
