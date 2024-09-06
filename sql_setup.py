import psycopg2
from database_key import db_host, db_name, db_pass, db_user

def create_table():
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
        )
    except:
        print("I am unable to connect to the database")
        raise ConnectionError
    
    with conn.cursor() as curs:
        curs.execute(f'''
                    DROP TABLE IF EXISTS dictionary;
                     
                    CREATE TABLE dictionary (
                        kana VARCHAR(32) NOT NULL,
                        kanji VARCHAR(16),
                        pos VARCHAR(16),
                        translation VARCHAR(96) NOT NULL,
                        chapter INTEGER NOT NULL,
                        PRIMARY KEY (kana, translation)
                    );     
                    ''')
        conn.commit()
        print("transaction finished")
        
if __name__ == "__main__":
    create_table()