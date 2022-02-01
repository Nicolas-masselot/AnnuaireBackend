from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from auth_db_connect import get_auth_connection, psycopg2
from annuaire_db_connect import get_annuaire_connection, psycopg2
app = Flask(__name__)

"""
Ce service doit permettre aux utilisateurs admin de :
- Ajouter/modifier/supprimer un utilisateur (mdp pouvant être réinitialisé)
- Promouvoir/rétrograder l'utilisateur (seulement pour le super admin)
"""
SUCCESSFUL_DB_CONNECT = "Connection to the PostgreSQL established successfully."
ERROR_DB_CONNECT = "Connection to the PostgreSQL encountered and error."


@app.route('/')
def hello():
    conn = get_annuaire_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM Personnes;'''
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)


@app.route('/users')
def getUsers():
    conn = get_auth_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM Users;'''
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)


@app.route('/users/getById')
def getUserById():
    conn = get_auth_connection()
    success = True
    error_set = []
    data = []

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    id_Users = request.form['id_Users']
    sql = "PREPARE getOneId (text) AS SELECT * FROM users WHERE id = $1; EXECUTE getOneId(%s);"

    cursor.execute(sql, id_Users)

    data = cursor.fetchall()
    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }
    conn.close()
    return jsonify(result)


@app.route('/users/create', methods=['POST'])
def createUsers():
    conn = get_auth_connection()
    success = True
    error_set = []
    data = []

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == 'POST' and 'loginUser' in request.form and 'password' in request.form and 'role' in request.form:
        loginUser = request.form['loginUser']
        password = request.form['password']
        role = request.form['role']

        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')

        # Check if account exists
        sql = "PREPARE checkExistUser (text) AS SELECT * FROM Users WHERE loginUser = $1 ; EXECUTE checkExistUser(%s);"
        cursor.execute(sql, (loginUser,))

        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            success = False
            error_set.append('USER_EXIST')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', loginUser):
            success = False
            error_set.append('INVALID_EMAIL')
        elif not loginUser or not password or not role:
            success = False
            error_set.append('INVALID_PARAMETERS')
        else:
            # Account does not exists and the form data is valid -> insert new account into Users table
            cursor.execute(
                "INSERT INTO USERS (loginUser, passwordUser, roleUser) VALUES (%s,%s,%s)", (loginUser, hashed_password, role))
            conn.commit()

            if (cursor.rowcount):
                success = True

                # Return created user
                cursor.execute(
                    'SELECT * FROM Users WHERE loginUser = %s', (loginUser))

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


# @app.route('/users/modify', methods=['PUT'])
# def modifyUsers():
#     conn = get_auth_connection()
#     success = True
#     error_set = []
#     data = []

#     if conn:
#         test_db = SUCCESSFUL_DB_CONNECT
#     else:
#         test_db = ERROR_DB_CONNECT
#     print(test_db)
#     cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

#     if request.method == 'PUT':

#     conn.close()
#     return jsonify(result)

@app.route('/users/modifyPassword', methods=['PUT'])
def modifyUsers():
    conn = get_auth_connection()
    success = True
    error_set = []
    data = []

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == 'PUT' and 'loginUser' in request.form and 'password' in request.form and 'newPassword' in request.form:
        loginUser = request.form['loginUser']
        password = request.form['password']
        newPassword = request.form['newPassword']

        cursor.execute(
            "SELECT password FROM Users  WHERE id_Users = %s;", (loginUser))
        current_Password = cursor.fetchone()

        if bcrypt.checkpw(password, current_Password):
            hashed_password = bcrypt.generate_password_hash(
                newPassword).decode('utf-8')
            cursor.execute(
                'UPDATE users SET password =  %s WHERE id_Users = %s', (newPassword, loginUser))
            # Fetch one record and return result
            update = cursor.fetchone()
            data.append(update)

        else:
            success = False
            error_set.append('PASSWORD_NOT_MATCH')
    elif request.method == 'PUT':
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


@app.route('/users/delete', methods=['DELETE'])
def deleteUsers():
    conn = get_auth_connection()
    success = True
    error_set = []
    data = []

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    if request.method == 'DELETE' and 'id_Users' in request.form:
        id_Users = request.form['id_Users']

        cursor.execute('DELETE FROM Users WHERE id_Users= %s', (id_Users,))

        # Fetch one record and return result
        account = cursor.fetchone()

        if (not account):
            success = False
            error_set.append('USER_EXIST')
        else:
            data.append(account)
    else:
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


@app.route('/users/upgrade', methods=['PUT'])
def upgradeUsers():

    conn = get_auth_connection()
    success = True
    error_set = []
    data = []

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if request.method == 'PUT' and 'id_Users' in request.form and 'current_Role' in request.form:
        current_Role = request.form['current_Role']
        id_Users = request.form['id_Users']

        if current_Role == 'user':
            cursor.execute(
                'UPDATE users SET role =  %s WHERE id_Users = %s', ('admin', id_Users))
            # Fetch one record and return result
            account = cursor.fetchone()

            data.append(account)
        elif current_Role == 'admin':
            cursor.execute(
                'UPDATE users SET role =  %s WHERE id_Users = %s', ('super_admin', id_Users))
            # Fetch one record and return result
            account = cursor.fetchone()

            data.append(account)
        else:
            # Form is empty
            success = False
            error_set.append('INVALID_PARAMETERS')

    elif request.method == 'PUT':
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


@app.route('/users/downgrade')
def downgradeUsers():

    conn = get_auth_connection()
    success = True
    error_set = []
    data = []

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    if request.method == 'PUT' and 'id_Users' in request.form and 'current_Role' in request.form:
        current_Role = request.form['current_Role']
        id_Users = request.form['id_Users']
        if current_Role == 'admin':
            cursor.execute(
                'UPDATE users SET role =  %s WHERE id_Users = %s', ('user', id_Users))
            # Fetch one record and return result
            account = cursor.fetchone()

            data.append(account)

        if current_Role == 'super_admin':
            cursor.execute(
                'UPDATE users SET role =  %s WHERE id_Users = %s', ('admin', id_Users))
            # Fetch one record and return result
            account = cursor.fetchone()

            data.append(account)
        else:
            # Form is empty
            success = False
            error_set.append('INVALID_PARAMETERS')

    elif request.method == 'PUT':
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7001, debug=True)
