from flask import Flask, request, redirect, jsonify, make_response
import requests

app = Flask(__name__)

AUTH_SERVER = 'https://centralserver-nxwp.onrender.com'  # Central server URL

@app.route('/')
def home():
    return '''
        <h1> Home </h1>
        <br>
        <a href="/dashboard"> Dashboard </a>
    '''
    
@app.route('/dashboard')
def dashboard():
    # Step 1: Check if the user has a session token (auth_token) in cookies
    token = request.cookies.get('auth_token')
    
    if not token:
        # Step 2: No token found, redirect to the central server for login
        return redirect(f'{AUTH_SERVER}/login?service=https://service1-cs.vercel.app/dashboard')

    # Step 3: If token exists, verify it with the central server
    response = requests.post(f'{AUTH_SERVER}/verify-token', data={'token': token})
    
    if response.status_code == 200 and response.json().get('valid'):
        # Step 4: If token is valid, allow access to dashboard
        username = response.json().get('username')
        return jsonify({"message": f"Welcome to NoctiService 1, {username}!"})
    
    # Step 5: If token verification fails, redirect to login again
    return "Authentication failed, please log in again.", 401


@app.route('/login_redirect')
def login_redirect():
    # Step 1: Retrieve the token from the central server redirect URL
    token = request.args.get('token')
    service = request.args.get('service')

    if not token:
        return "Error: No token provided", 400

    # Set a cookie with the token
    response = make_response(redirect('/final_redirect?service=' + service))
    response.set_cookie(
        'auth_token',
        token,
        httponly=True,
        secure=True,
        domain='service1-cs.vercel.app',  # Set for *.vercel.app
        samesite='None'
    )
    print("Cookie set with token:", token)  # Add this debug statement
    
    return response

@app.route('/final_redirect')
def final_redirect():
    service = request.args.get('service')
    if not service:
        return "Error: No service URL provided", 400

    # Redirect to the service URL
    return redirect(service)


if __name__ == "__main__":
    app.run(debug=True)
