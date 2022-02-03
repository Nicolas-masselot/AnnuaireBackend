import re
from flask import Flask , request, jsonify
from flask_cors import CORS
from db_connect import get_connection , psycopg2

SUCCESSFUL_DB_CONNECT = "Connection to the PostgreSQL established successfully."
ERROR_DB_CONNECT = "Connection to the PostgreSQL encountered and error."

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/v1/personnes/getAllPersonnes', methods = ['POST'])
def getAllPersonnes():
    
    success = True
    error_set = []
    data = []

    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
        success = False
        error_set.append(test_db)

    print(test_db)

    if(success):  
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        sql = '''SELECT * FROM Personnes;'''
        cursor.execute(sql)
        data = cursor.fetchall()
        conn.close()

    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }   
    return jsonify(result)
  
@app.route('/api/v1/personnes/getPersonneByMail', methods = ['POST'])
def getPersonneByMail():
    success = True
    error_set = []
    data = []

    req = request.get_json()

    mailrecherche = req.get("email")
    if(mailrecherche != None):
        mailrecherche = '%'+mailrecherche+'%'
    else:
        success = False
        error_set.append('INVALID PARAMETERS')
    

    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
        success = False
        error_set.append(test_db)

    print(test_db)

    if(success):
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        sql = "PREPARE getPersMail (text) AS SELECT * FROM Personnes WHERE email LIKE $1 ; EXECUTE getPersMail(%s);"
        cursor.execute(sql,(mailrecherche,))
        data = cursor.fetchall()
        conn.close()

    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }  
    return jsonify(result)

@app.route('/api/v1/personnes/getPersonneByPhone', methods = ['POST'])
def getPersonneByPhone():
    req = request.get_json()

    phonerecherche = req.get("tel")
    success = True
    error_set = []
    data = []


    if(phonerecherche == None):
        success = False
        error_set.append('INVALID PARAMETERS')

    

    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
        success = False
        error_set.append(test_db)

    print(test_db)
    if(success):
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        sql = "PREPARE getPersPhone (text) AS SELECT * FROM Personnes WHERE tel = $1 ; EXECUTE getPersPhone(%s);"
        cursor.execute(sql,(phonerecherche,))
        data = cursor.fetchall()
        conn.close()

    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }
    return jsonify(result)
  
@app.route('/api/v1/personnes/getPersonneByNoms', methods = ['POST'])
def getPersonneByNoms():

    success = True
    error_set = []
    data = []

    req = request.get_json()

    nomrecherche = req.get("nom")
    prenomrecherche = req.get("prenom")

    conn = get_connection()

    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
        success = False
        error_set.append(test_db)

    print(test_db)
    cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
    if(nomrecherche == None and prenomrecherche != None and success):
        prenomrecherche = '%'+prenomrecherche+'%'
        sql = "PREPARE getPersPrenom (text) AS SELECT * FROM Personnes WHERE prenom ILIKE $1 ; EXECUTE getPersPrenom(%s);"
        cursor.execute(sql,(prenomrecherche,))
        data = cursor.fetchall()
        conn.close()
    elif(prenomrecherche == None and nomrecherche != None and success):
        nomrecherche = '%'+nomrecherche+'%'
        sql = "PREPARE getPersNom (text) AS SELECT * FROM Personnes WHERE nom ILIKE $1 ; EXECUTE getPersNom(%s);"
        cursor.execute(sql,(nomrecherche,))
        data = cursor.fetchall()
        conn.close()
    elif(prenomrecherche != None and nomrecherche != None and success):
        nomrecherche = '%'+nomrecherche+'%'
        prenomrecherche = '%'+prenomrecherche+'%'
        sql = "PREPARE getPersNomPrenom (text,text) AS SELECT * FROM Personnes WHERE nom ILIKE $1 AND prenom ILIKE $2 ; EXECUTE getPersNomPrenom(%s,%s);"
        cursor.execute(sql,(nomrecherche,prenomrecherche))
        data = cursor.fetchall()
        conn.close()
    else:
        success = False
        error_set.append('INVALID PARAMETERS')
        
    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }
    return jsonify(result)

@app.route('/api/v1/personnes/getPersonneByID', methods = ['POST'])
def getPersonneByID():
    success = True
    error_set = []
    data = []
    req = request.get_json()
    
    IDrecherche = req.get("idPers")
    if(IDrecherche == None):
        success = False
        error_set.append('INVALID PARAMETERS')
    

    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
        success = False
        error_set.append(test_db)

    print(test_db)

    if(success):
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        sql = "PREPARE getPersID (int) AS SELECT * FROM Personnes WHERE id_Personnes = $1 ; EXECUTE getPersID(%s);"
        cursor.execute(sql,(IDrecherche,))
        data = cursor.fetchall()
        conn.close()

    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }  
    return jsonify(result)


@app.route('/api/v1/personnes/ModifyPersonne', methods = ['POST'])
def ModifyPersonne():
    success = True
    error_set = []
    data = []
    req = request.get_json()
    
    IDpers = req.get("idPers")
    Adresse = req.get("adresse")
    Code_postal = req.get("codepostal")
    Mail = req.get("email")
    Nom = req.get("nom")
    Prenom = req.get("prenom")
    Tel= req.get("tel")
    Ville =  req.get("ville") 

    if(IDpers == None or Adresse == None or Code_postal == None or Mail == None or Nom == None or Prenom == None or Tel == None or Ville == None ):
        success = False
        error_set.append('INVALID PARAMETERS')
    

    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
        success = False
        error_set.append(test_db)

    print(test_db)

    if(success):
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        sql = "PREPARE EditPers (int ,text,text,text,text,text,text,text) AS UPDATE Personnes SET nom = $2,prenom = $3 , tel = $4 , adresse = $5 , code_postal = $6 , ville = $7 , email = $8 WHERE id_Personnes = $1 ; EXECUTE EditPers(%s ,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(sql,(IDpers , Nom , Prenom ,Tel , Adresse , Code_postal , Ville , Mail ))
        conn.commit()
        conn.close()

    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }  
    return jsonify(result)


@app.route('/api/v1/personnes/AddPersonne', methods = ['POST'])
def AddPersonne():
    success = True
    error_set = []
    data = []
    req = request.get_json()
    
    IDpers = req.get("idPers")
    Adresse = req.get("adresse")
    Code_postal = req.get("codepostal")
    Mail = req.get("email")
    Nom = req.get("nom")
    Prenom = req.get("prenom")
    Tel= req.get("tel")
    Ville =  req.get("ville") 

    if(IDpers == None or Adresse == None or Code_postal == None or Mail == None or Nom == None or Prenom == None or Tel == None or Ville == None ):
        success = False
        error_set.append('INVALID PARAMETERS')
    

    conn = get_connection()
    if conn:
        test_db = SUCCESSFUL_DB_CONNECT
    else:
        test_db = ERROR_DB_CONNECT
        success = False
        error_set.append(test_db)

    print(test_db)

    if(success):
        cursor = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)
        sql = "PREPARE EditPers (int ,text,text,text,text,text,text,text) AS INSERT INTO Personnes Values($1, $2, $3 , $4 , $5 ,  $6 , $7 , $8) ; EXECUTE EditPers(%s ,%s,%s,%s,%s,%s,%s,%s);"
        cursor.execute(sql,(IDpers , Nom , Prenom ,Tel , Adresse , Code_postal , Ville , Mail ))
        conn.commit()
        conn.close()

    result = {
        "status": 200,
        "success": success,
        "errorSet": error_set,
        "data": data
    }  
    return jsonify(result)


if __name__ == "__main__":
    app.run(host ='0.0.0.0', port = 5001, debug = True) 