from flask import Flask , jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import re
from db_connect import get_connection , psycopg2

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
bcrypt = Bcrypt()
bcrypt.init_app(app)

SUCCESSFUL_DB_CONNECT = "Connection to the PostgreSQL established successfully."
ERROR_DB_CONNECT = "Connection to the PostgreSQL encountered and error."

@app.route('/api/v1/users/login', methods=['POST'])
def login():
    conn = get_connection()

    success = True
    error_set = []
    data = []

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT

    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
   
    # Check if "login" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'login' in request.form and 'password' in request.form:
        login = request.form['login']
        password = request.form['password']
 
        # Check if account exists 
        sql = "PREPARE checkExistUser (text) AS SELECT * FROM Users WHERE loginUser = $1 ; EXECUTE checkExistUser(%s);"
        cursor.execute(sql,(login,))
        # cursor.execute('SELECT * FROM Users WHERE loginUser = %s', (login,))
        
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_respond = account['passworduser']
            # If account exists in users table in out database
            if bcrypt.check_password_hash(password_respond, password):
                success = True
                data.append(account)
            else:
                # incorrect password 
                success = False
                error_set.append('INCORRECT_PASSWORD')
        else:
            # Account does not exist 
            success = False
            error_set.append('USER_NOT_FOUND')
    else:
        success = False
        error_set.append('INVALID_PARAMETERS')

    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }
    
    conn.close()

    return jsonify(result)

@app.route('/api/v1/users/register', methods=['POST'])
def register():
    conn = get_connection()

    success = True
    error_set = []
    data = []

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT

    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
 
    # Check if "login", "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'login' in request.form and 'password' in request.form and 'role' in request.form:
        login = request.form['login']
        password = request.form['password']
        role = request.form['role']
    
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
 
        # Check if account exists 
        sql = "PREPARE checkExistUser (text) AS SELECT * FROM Users WHERE loginUser = $1 ; EXECUTE checkExistUser(%s);"
        cursor.execute(sql,(login,))

        # Fetch one record and return result
        account = cursor.fetchone()

        # If account exists show error and validation checks
        if account:
            success = False
            error_set.append('USER_EXIST')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', login):
            success = False
            error_set.append('INVALID_EMAIL')
        elif not login or not password or not role:
            success = False
            error_set.append('INVALID_PARAMETERS')
        else:
            # Account does not exists and the form data is valid -> insert new account into Users table
            cursor.execute("INSERT INTO USERS (loginUser, passwordUser, roleUser) VALUES (%s,%s,%s)", (login, hashed_password, role))
            conn.commit()

            if (cursor.rowcount):
                success = True

                # Return created user
                cursor.execute('SELECT * FROM Users WHERE loginUser = %s', (login,))
                
                # Fetch one record and return result
                account = cursor.fetchone()

                data.append(account)
            else:
                success = False
                error_set.append('ERROR_SYSTEM')

    elif request.method == 'POST':
        # Form is empty
        success = False
        error_set.append('INVALID_PARAMETERS')

    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }
    
    conn.close()

    return jsonify(result)