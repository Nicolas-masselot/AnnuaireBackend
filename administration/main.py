from flask import Flask, jsonify, request
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

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    _id = request.form['_id']
    sql = "PREPARE getOneId (text) AS SELECT * FROM users WHERE id = $1; EXECUTE getOneId(%s);"

    cursor.execute(sql, _id)

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

    conn.close()
    return jsonify(results)


@app.route('/users/modify', methods=['PUT'])
def modifyUsers():
    conn = get_auth_connection()
    conn.close()
    return jsonify(results)


@app.route('/users/delete', methods=['DELETE'])
def deleteUsers():
    conn = get_auth_connection()
    conn.close()
    return jsonify(results)


@app.route('/users/upgrade')
def upgradeUsers():
    conn = get_auth_connection()
    conn.close()
    return jsonify(results)


@app.route('/users/downgrade')
def downgradeUsers():
    conn = get_auth_connection()
    conn.close()
    return jsonify(results)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7001, debug=True)
