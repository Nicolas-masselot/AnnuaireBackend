from flask import Flask, jsonify
from auth_db_connect import get_auth_connection, psycopg2
from annuaire_db_connect import get_annuaire_connection, psycopg2
app = Flask(__name__)

"""
Ce service doit permettre aux utilisateurs admin de :
- Ajouter/modifier/supprimer un utilisateur (mdp pouvant être réinitialisé)
- Promouvoir/rétrograder l'utilisateur (seulement pour le super admin)
"""


@app.route('/')
def hello():
    conn = get_annuaire_connection()
    if conn:
        test_db = "Connection to the PostgreSQL established successfully."
    else:
        test_db = "Connection to the PostgreSQL encountered and error."
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
        test_db = "Connection to the PostgreSQL established successfully."
    else:
        test_db = "Connection to the PostgreSQL encountered and error."
    print(test_db)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM Users;'''
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)


@app.route('/users/create')
def createUsers():
    conn = get_auth_connection()
    conn.close()
    return jsonify(results)


@app.route('/users/modify')
def modifyUsers():
    conn = get_auth_connection()
    conn.close()
    return jsonify(results)


@app.route('/users/delete')
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
