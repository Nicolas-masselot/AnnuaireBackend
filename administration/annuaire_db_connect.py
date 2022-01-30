import psycopg2
import psycopg2.extras
  
def get_annuaire_connection():
    try:
        return psycopg2.connect(
            database="annuaire",
            user="annuaire_user",
            password="annuaire",
            host="db_annuaire",
            port=5432,
        )
    except Exception as e:
        print(e)
        return False