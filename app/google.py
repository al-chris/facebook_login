from flask import Flask, redirect, request, session, jsonify, render_template
from requests_oauthlib import OAuth2Session
from app import app
import os

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
# REDIRECT_URI = 'http://localhost:5000/callback'  # Set this to your callback URL
GOOGLE_REDIRECT_URI = 'https://test-auth-i2mu.onrender.com/google/callback'

# Google OAuth endpoints
GOOGLE_AUTHORIZATION_BASE_URL = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_URL = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'



@app.route('/login/google')
def google_login():
    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=GOOGLE_REDIRECT_URI, scope=['profile', 'email'])
    authorization_url, state = google.authorization_url(GOOGLE_AUTHORIZATION_BASE_URL, access_type='offline')

    # Save the state to compare it in the callback
    session['oauth_state'] = state

    return redirect(authorization_url)

@app.route('/google/callback')
def google_callback():
    # Check for CSRF attacks
    # if request.args.get('state') != session.pop('oauth_state', None):
    #     return 'Invalid state'

    google = OAuth2Session(GOOGLE_CLIENT_ID, redirect_uri=GOOGLE_REDIRECT_URI)
    token = google.fetch_token(GOOGLE_TOKEN_URL, client_secret=GOOGLE_CLIENT_SECRET, authorization_response=request.url)

    # Use the token to make a request to the Google API to get user data
    response = google.get(GOOGLE_USER_INFO_URL)

    if response.status_code == 200:
        user_data = response.json()
        print(user_data)
        # Return the user's data (you can customize this response as needed)
        return render_template("dashboard.html", user_data=user_data)
    else:
        return 'Failed to fetch user data from Google API'



# {
#     'id': '101278525397366933741',
#     'email': 'christopheraliu07@gmail.com',
#     'verified_email': True,
#     'name': 'Al Chris',
#     'given_name': 'Al',
#     'family_name': 'Chris',
#     'picture': 'https://lh3.googleusercontent.com/a/ACg8ocIZOw30iSLXQIvvU7B9OkqtGFc0WYhmP2dcapuAAnKU4z0WntnP=s96-c',
#     'locale': 'en-GB'
# }