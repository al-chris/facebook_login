from flask import Flask, render_template
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or "dont guess me"


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/terms_of_service')
def t_o_s():
    return render_template("terms_of_service.html")

@app.route('/privacy_policy')
def privacy():
    return render_template("privacy_policy.html")

from app import facebook, tiktok, google, jwt