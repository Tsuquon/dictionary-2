import psycopg2
from database_key import db_host, db_name, db_pass, db_user
import pandas as pd

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

def insert_into_database(df):
    try:
        conn = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pass,
        )
    except ConnectionError:
        print("Error: Unable to connect to the database.")
        raise ConnectionError
    
    sql = """
        INSERT INTO dictionary VALUES (
            %s, %s, %s, %s, %s
        );
    """
    
    with conn.cursor() as curs:
        data = df.where(pd.notnull(df), None).values.tolist()
        curs.executemany(sql, data)
        conn.commit()
        print("data inserted")
      
def clean_df() -> pd.DataFrame:
    xlsx_file = "genki_words.xlsx"
    data_file = pd.ExcelFile(xlsx_file)
    read_file = pd.read_excel(data_file, sheet_name="Sheet1")
    formatted_df = read_file.drop('No.', axis=1)
    
    def extract_chapter(chapter):
        import re
        numbers = re.findall(r'\d+', chapter)
        if numbers:
            return min(map(int, numbers))
        if 'G' in str(chapter):
            return 0
        return chapter

    formatted_df['chapter'] = formatted_df['chapter'].apply(extract_chapter)
    
    # # Replace empty values with null
    # formatted_df = formatted_df.replace('NaN', None)
    
    # print(formatted_df.loc[70])
    return formatted_df

if __name__ == "__main__":
    create_table()
    dfs = clean_df()
    insert_into_database(dfs)