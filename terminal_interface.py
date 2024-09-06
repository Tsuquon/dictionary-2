from database_key import db_host, db_name, db_pass, db_user
import psycopg2
import random

class TerminalInterface:
    def __init__(self):
        pass
    
        
    def input_interface(self):
        while (user_input:=input("""
Choose from the options below:
1. Chapter Selection

                    """)) != "exit":
            if user_input == "1":
                self.choose_chapter()
                
    def choose_chapter(self):
        while (user_input:=input("Choose a chapter number:\n")) != "exit":
            if not user_input.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            chapter_number = int(user_input)
            break

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
            SELECT *
            FROM dictionary
            WHERE chapter = %s
        """

        with conn.cursor() as curs:

            curs.execute(sql, (chapter_number,))
            word_bank = curs.fetchall()
            
        print(word_bank)
        self.choose_quantity(word_bank)
        
    # eventually allow all
    def choose_quantity(self, word_bank):
        while (user_input:=input("Choose a quantity:\n")) != "exit":
            if not user_input.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            quantity = int(user_input)
            break
        
        
        if quantity > len(word_bank):
            print(f"Warning: Requested quantity ({quantity}) is greater than the available words ({len(word_bank)}). Using all available words.")
            quantity = len(word_bank)
        
        selected_words = random.sample(word_bank, quantity)
        print(selected_words)
        # return selected_words
        
        
        
        
        