from flask import Flask, request, jsonify
import pymysql
import bcrypt

app = Flask(__name__)

# MySQL configuration
conn = pymysql.connect(
    host='localhost',
    user='haekals',
    password='Perdana@2022',
    db='ams'
)

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
    
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = %s  AND token = md5(%s)", (user_id,token,))
    hashed_password = cursor.fetchone()[0]
    if bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8')):
        # Define the SELECT statement
        select_stmt = "SELECT 1 FROM assets_active_time WHERE email = %s"
        # Execute the SELECT statement with the desired value
        cursor.execute(select_stmt, (user_id,))
        # Fetch the result
        result = cursor.fetchone()
        # Check if the result is None (record does not exist) or not (record exists)
        if result is None:
            # INSERT statement
            cursor.execute("INSERT INTO assets_active_time (email,assets_active_time,hostname,assets_last_boot,working_hours,ipAddrLocal,assets_location,usr_first_login,last_updated) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)", (user_id,uptime,hostname,last_boot,workHours,ipAddrLocal,ipAddr,usr_first_login,last_updated))
            conn.commit()
        else:
            cursor.execute("UPDATE assets_active_time SET assets_active_time = %s, hostname = %s, assets_last_boot = %s,working_hours = %s,ipAddrLocal = %s, assets_location = %s, usr_first_login = %s, last_updated = %s WHERE email = %s", (uptime,hostname,last_boot,workHours,ipAddrLocal,ipAddr,usr_first_login,last_updated,user_id))
            conn.commit()
        print(data)
        return jsonify({'message': 'Successfully sent to database'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

    

if __name__ == '__main__':
    app.run(debug=False)