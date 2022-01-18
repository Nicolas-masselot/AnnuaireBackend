﻿from flask import Flask , jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
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
    print(test_db)

    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
   
    # Check if "login" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'login' in request.form and 'password' in request.form:
        login = request.form['login']
        password = request.form['password']
 
        # Check if account exists using MySQL
        sql = "PREPARE checkExistUser (text) AS SELECT * FROM Users WHERE loginUser = $1 ; EXECUTE checkExistUser(%s);"
        cursor.execute(sql,(login,))
        # cursor.execute('SELECT * FROM Users WHERE loginUser = %s', (login,))
        
        # Fetch one record and return result
        account = cursor.fetchone()
 
        if account:
            password_respond = account['passworduser']
            # If account exists in users table in out database
            # if bcrypt.check_password_hash(password_respond, password):
            if password_respond == password:
                success = True
                data.append(account)
            else:
                # password incorrect
                success = False
                error_set.append('PASSWORD_INCORRECT')
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

@app.route('/')
def hello():
    conn = get_connection()
    if conn:
        test_db = "Connection to the PostgreSQL established successfully."
    else:
        test_db = "Connection to the PostgreSQL encountered and error."
    print(test_db)
    print(conn)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM Users;'''
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)
  
  
if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 6001, debug = True) 