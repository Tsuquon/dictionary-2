
from openai import OpenAI
import pandas as pd
import psycopg2
from database_key import db_host, db_name, db_pass, db_user
from terminal_interface import TerminalInterface

def llm_prompt():
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": "write a haiku about ai"}
        ]
    )
    
    
# probably move this into sql setup    
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
        curs.executemany(sql, df.values.tolist())
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
    
    print(formatted_df.loc[70])
    return formatted_df




def main():
    interface = TerminalInterface()
    interface.input_interface()
    # df = clean_df()
    # insert_into_database(df)


if __name__ == "__main__":
    main()
    
