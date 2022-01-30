import psycopg2
import psycopg2.extras
  
def get_auth_connection():
    try:
        return psycopg2.connect(
            database="auth",
            user="auth_user",
            password="auth",
            host="db_auth",
            port=5432,
        )
    except Exception as e:
        print(e)
        return False