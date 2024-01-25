from flask import Flask, redirect, request, session, url_for
import facebook

app = Flask(__name__)
app.secret_key = 'you@wontguessit'  # Replace with a secure secret key

@app.route('/')
def index():
    if 'access_token' in session:
        graph = facebook.GraphAPI(access_token=session['access_token'])
        user_info = graph.get_object('me')
        return f"Logged in as: {user_info['name']} (ID: {user_info['id']})"
    else:
        return 'Not logged in.'

@app.route('/login')
def login():
    return redirect(get_facebook_login_url())

@app.route('/callback')
def callback():
    code = request.args.get('code')
    access_token = get_access_token(code)
    session['access_token'] = access_token
    return redirect(url_for('index'))

def get_facebook_login_url():
    app_id = 'your_app_id'
    redirect_uri = url_for('callback', _external=True)
    graph = facebook.GraphAPI()
    return graph.get_auth_url(app_id, redirect_uri, scope=['email'])

def get_access_token(code):
    app_id = 'your_app_id'
    app_secret = 'your_app_secret'
    redirect_uri = url_for('callback', _external=True)
    graph = facebook.GraphAPI()
    response = graph.get_access_token_from_code(code, app_id, app_secret, redirect_uri)
    return response['access_token']

if __name__ == '__main__':
    app.run(debug=True)
