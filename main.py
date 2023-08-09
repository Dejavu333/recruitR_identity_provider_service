from flask import Flask, request, jsonify
import jwt
import datetime
import os

####################################################
# setup 
####################################################
# webapp
app = Flask(__name__)
# key to sign the JWT
PRIVATE_KEY = os.getenv("PRIVATE_KEY_ENVV", "supersecret")
# db
users = {"testuser": "testpassword"}

####################################################
# routes
####################################################
@app.route('/register', methods=['POST'])
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    if username in users:
        return jsonify({"error": "User already exists!"}), 400
    users[username] = password
    return jsonify({"message": "User registered successfully!"}), 201

@app.route('/authN', methods=['POST'])
def authenticate():
    username = request.json.get("username")
    password = request.json.get("password")

    if users.get(username) == password:
        token = jwt.encode({
            'user': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, PRIVATE_KEY)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials!"}), 401

@app.route('/authZ', methods=['GET'])
def authorize():
    token = request.headers.get("Authorization").split(" ")[1]
    try:
        decoded = jwt.decode(token, PRIVATE_KEY, algorithms=["HS256"])
        return jsonify({"user": decoded["user"], "message": "Authorized!"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired!"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token!"}), 401

####################################################
# main
####################################################
if __name__ == '__main__':
    app.run()