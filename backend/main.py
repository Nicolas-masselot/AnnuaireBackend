from flask import Flask , request, jsonify
from db_connect import get_connection , psycopg2

SUCCESSFUL_DB_CONNECT = "Connection to the PostgreSQL established successfully."
ERROR_DB_CONNECT = "Connection to the PostgreSQL encountered and error."
app = Flask(__name__)

@app.route('/getAllPersonnes', methods = ['POST'])
def getAllPersonnes():
    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = '''SELECT * FROM Personnes;'''
    cursor.execute(sql)
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)
  
@app.route('/getPersonnebyMail', methods = ['POST'])
def getPersonneByMail():
    mailrecherche = request.form.get("email")
    mailrecherche = '%'+mailrecherche+'%'
    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "PREPARE getPersMail (text) AS SELECT * FROM Personnes WHERE email LIKE $1 ; EXECUTE getPersMail(%s);"
    cursor.execute(sql,(mailrecherche,))
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)

@app.route('/getPersonnebyPhone', methods = ['POST'])
def getPersonneByPhone():
    phonerecherche = request.form.get("tel")
    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    sql = "PREPARE getPersPhone (text) AS SELECT * FROM Personnes WHERE tel = $1 ; EXECUTE getPersPhone(%s);"
    cursor.execute(sql,(phonerecherche,))
    results = cursor.fetchall()
    conn.close()
    return jsonify(results)
  
@app.route('/getPersonnebyNoms', methods = ['POST'])
def getPersonneByNoms():
    nomrecherche = request.form.get("nom")
    prenomrecherche = request.form.get("prenom")
    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
    print(test_db)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    if(nomrecherche == None and prenomrecherche != None):
        prenomrecherche = '%'+prenomrecherche+'%'
        sql = "PREPARE getPersPrenom (text) AS SELECT * FROM Personnes WHERE prenom ILIKE $1 ; EXECUTE getPersPrenom(%s);"
        cursor.execute(sql,(prenomrecherche,))
        results = cursor.fetchall()
        conn.close()
    elif(prenomrecherche == None and nomrecherche != None):
        nomrecherche = '%'+nomrecherche+'%'
        sql = "PREPARE getPersNom (text) AS SELECT * FROM Personnes WHERE nom ILIKE $1 ; EXECUTE getPersNom(%s);"
        cursor.execute(sql,(nomrecherche,))
        results = cursor.fetchall()
        conn.close()
    elif(prenomrecherche != None and nomrecherche != None):
        nomrecherche = '%'+nomrecherche+'%'
        prenomrecherche = '%'+prenomrecherche+'%'
        sql = "PREPARE getPersNomPrenom (text,text) AS SELECT * FROM Personnes WHERE nom ILIKE $1 AND prenom ILIKE $2 ; EXECUTE getPersNomPrenom(%s,%s);"
        cursor.execute(sql,(nomrecherche,prenomrecherche))
        results = cursor.fetchall()
        conn.close()
        
    return jsonify(results)

if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = True) 