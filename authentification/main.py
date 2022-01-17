from flask import Flask , jsonify
from db_connect import get_connection , psycopg2
app = Flask(__name__)
  
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