from flask import Flask, redirect, request, session, jsonify
from requests_oauthlib import OAuth2Session
from app import app

# TikTok OAuth configuration
CLIENT_ID = ''
CLIENT_SECRET = ''
# REDIRECT_URI = 'http://localhost:5000/tiktok/callback'  # Set this to your callback URL
REDIRECT_URI = 'https://test-auth-i2mu.onrender.com/tiktok/callback'

# TikTok OAuth endpoints
AUTHORIZATION_BASE_URL = 'https://open-api.tiktok.com/oauth/authorize'
TOKEN_URL = 'https://open-api.tiktok.com/oauth/access_token'


@app.route('/login/tiktok')
def tiktok_login():
    tiktok = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=['user.info'])
    authorization_url, state = tiktok.authorization_url(AUTHORIZATION_BASE_URL)

    # Save the state to compare it in the callback
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route('/tiktok/callback')
def tiktok_callback():
    # Check for CSRF attacks
    # if request.args.get('state') != session.pop('oauth_state', None):
    #     return 'Invalid state'

    tiktok = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    token = tiktok.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET, authorization_response=request.url)

    # Use the token to make a request to the TikTok API to get user data
    user_info_url = 'https://open-api.tiktok.com/me'
    headers = {'Authorization': f'Bearer {token["access_token"]}'}
    response = tiktok.get(user_info_url, headers=headers)

    if response.status_code == 200:
        user_data = response.json()
        # Return the user's data (you can customize this response as needed)
        return jsonify(user_data), 200
    else:
        return 'Failed to fetch user data from TikTok API'

