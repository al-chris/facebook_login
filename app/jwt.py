from flask import Flask, request, jsonify
import jwt #pip install PyJWT
from app import app

@app.route('/login', methods=['POST'])
def login():
    # Get username and password from request
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if username and password are valid (you need to implement this part)

    # If valid, create a JWT token
    payload = {'username': username}
    token = jwt.encode(payload, 'secret', algorithm='HS256')

    return jsonify({'token': token.decode('UTF-8')})

@app.route('/protected', methods=['GET'])
def protected():
    # Get token from the Authorization header
    token = request.headers.get('Authorization')

    # Decode the token
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        return jsonify({'message': 'Welcome, {}!'.format(payload['username'])})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired. Please log in again.'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token. Please log in.'}), 401
