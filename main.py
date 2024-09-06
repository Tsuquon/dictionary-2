
import random
from openai import OpenAI
import pandas as pd
import psycopg2
from database_key import db_host, db_name, db_pass, db_user
from terminal_interface import TerminalInterface
from llm_response_format import LLMResponseFormat

def llm_prompt(def_word, usr_word):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are going to read off a tuple giving the kana and kanji (if available). The user will respond in english, and you will check if the definition matches closely enough to the given translation in the word bank"},
            {"role": "system", "content": "The format of the tuple is structured as (kana, kanji (opt), pos, definition, chapter number)"},
            {"role": "system", "content": "your response, followed by boolean if it was correct or not"},
            {"role": "system", "content": f"The given word is {def_word}"},
            {"role": "user", "content": f"Is the answer {usr_word}"}
        ],
        response_format=LLMResponseFormat
    )
    print(completion.choices[0].message.content)
    

    
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
    word_bank = interface.input_interface()
    # llm_prompt(word_bank)
    random.shuffle(word_bank)
    for word in word_bank:
        user_input = input(f"Enter the translation for {word[0]}: ")
        # print(word)
        llm_prompt(word, user_input)
    
    # df = clean_df()
    # insert_into_database(df)


if __name__ == "__main__":
    main()
    
