from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import jwt
import pymysql
import json
import os

app = Flask(__name__)

# Secret key for generating JWT tokens
import secrets

SECRET_KEY = secrets.token_hex(10)

# MySQL configuration
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='password',
    db='aps'
)

# Function to generate JWT tokens
def generate_token(user_id):
    payload = {
        'sub': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=59)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

# Function to verify JWT tokens
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Token expired. Please login again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please login again.'



# API endpoint to access protected resources
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    # Get the user's credentials from the request body
    user_id = data['user_id']
    password = data['password']
    token = data['token']

    # Authenticate user
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s AND token = %s", (user_id, password,token))
    user = cur.fetchone()
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401
    print(data)
    return jsonify({'message': 'Successfully Connected to API Endpoint'})



# API endpoint to generate a token
@app.route('/generate', methods=['POST'])
def generate():
    # Get the user's credentials from the request body
    data = request.get_json()
    user_id = data.get('user_id')
    password = data.get('password')
    # Authenticate user
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (user_id, password))
    user = cur.fetchone()
    if not user:
        return jsonify({'message': 'User Not Found'}), 401
    token = generate_token(user_id)
    # Insert JWT and user information into MySQL table
    cur.execute("UPDATE users SET token = %s WHERE email = %s", (token, user_id))
    conn.commit()
    return jsonify({'token': token})



# API endpoint to access protected resources
@app.route('/endpoint', methods=['POST'])
def endpoint():
    # Get the user's credentials from the request body
    data = request.get_json()
    user_id = data['user_id']
    password = data['password']
    token = data['token']
    hostname = data['hostname']
    workHours = data['workHours']
    ipAddr = data['ipAddr']
    ipAddrLocal = data['ipAddrLocal']
    last_boot = data["last_boot"]
    uptime = data["uptime_since_last_boot"]
    usr_first_login = data["usr_first_login"]
    last_updated = data["last_updated"]

    #Retrieve data from local json files
    # username = os.getlogin()
    # file_path = os.path.join("C:", "Users", username, "Documents", "data", "data.json")
    # os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # with open(file_path, "r") as infile:
    #     data = json.load(infile)

    # user_id = data['user_id']
    # password = data['password']
    # token = data['token']

    # print(data['name'])

    # Authenticate user
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s AND token = %s", (user_id, password,token))
    user = cur.fetchone()
    if not user:
        return jsonify({'message': 'Invalid credentials'}), 401

    # Define the SELECT statement
    select_stmt = "SELECT 1 FROM assets_active_time WHERE email = %s"

    # Execute the SELECT statement with the desired value
    cur.execute(select_stmt, (user_id,))

    # Fetch the result
    result = cur.fetchone()

    # Check if the result is None (record does not exist) or not (record exists)
    if result is None:
        # INSERT statement
        cur.execute("INSERT INTO assets_active_time (email,assets_active_time,hostname,assets_last_boot,working_hours,ipAddrLocal,assets_location,usr_first_login,last_updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (user_id,uptime,hostname,last_boot,workHours,ipAddrLocal,ipAddr,usr_first_login,last_updated))
        conn.commit()
    else:
        cur.execute("UPDATE assets_active_time SET assets_active_time = %s, hostname = %s, assets_last_boot = %s,working_hours = %s,ipAddrLocal = %s, assets_location = %s, usr_first_login = %s, last_updated = %s WHERE email = %s", (uptime,hostname,last_boot,workHours,ipAddrLocal,ipAddr,usr_first_login,last_updated,user_id))
        conn.commit()

    # cur.execute("UPDATE assets_active_time SET assets_active_time = %s, hostname = %s, assets_last_boot = %s,working_hours = %s,ipAddrLocal = %s, assets_location = %s, usr_first_login = %s, last_updated = %s WHERE email = %s", (uptime,hostname,last_boot,workHours,ipAddrLocal,ipAddr,usr_first_login,last_updated,user_id))
    # cur.execute("INSERT INTO assets_active_time (email,assets_active_time,hostname,assets_last_boot,working_hours,ipAddrLocal,assets_location,usr_first_login,last_updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (user_id,uptime,hostname,last_boot,workHours,ipAddrLocal,ipAddr,usr_first_login,last_updated))
    # conn.commit()
    print(data)
    return jsonify({'message': 'Successfully sent to database'})

if __name__ == '__main__':
    app.run()

# host="10.1.201.39", port=8000, debug=True
# ISSUE DI DIRECTORY FOLDER data.json