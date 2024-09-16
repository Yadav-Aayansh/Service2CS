from flask import Flask, request, redirect, jsonify, make_response
import requests

app = Flask(__name__)
AUTH_SERVER = 'https://centralserver.onrender.com'  # Auth server URL

@app.route('/dashboard')
def dashboard():
    # Check if the user has a valid session token
    token = request.cookies.get('session_token')
    if not token:
        # No token, redirect to the auth server for login
        return redirect(f'{AUTH_SERVER}/login?service=https://noctiservice2.vercel.app/dashboard')
    
    # Verify the token with the auth server
    response = requests.post(f'{AUTH_SERVER}/verify-token', data={'token': token})
    if response.json().get('valid'):
        return jsonify({"message": f"Welcome to NoctiService 2, {response.json()['username']}!"})
    else:
        return "Authentication failed, please log in again.", 401

@app.route('/dashboard', methods=['GET'])
def login_redirect():
    token = request.args.get('token')
    if token:
        # Set a session cookie with the token
        response = make_response(redirect('/dashboard'))
        response.set_cookie('session_token', token)
        return response
    return "Error: No token provided", 400

if __name__ == '__main__':
    app.run(debug=True)
