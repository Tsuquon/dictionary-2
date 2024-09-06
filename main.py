
import random
import pandas as pd
import psycopg2
from database_key import db_host, db_name, db_pass, db_user
from terminal_interface import TerminalInterface


    
    

    
# probably move this into sql setup    



def main():
    interface = TerminalInterface()
    interface.run_program()
    
        
    # word_bank = interface.input_interface()
    # llm_prompt(word_bank)
    # random.shuffle(word_bank)
    # for word in word_bank:
        # user_input = input(f"Enter the translation for {word[0]}: ")
    #     # print(word)
    #     llm_prompt(word, user_input)
    
    # df = clean_df()
    # insert_into_database(df)


if __name__ == "__main__":
    main()
    
