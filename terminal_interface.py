from database_key import db_host, db_name, db_pass, db_user
import psycopg2
import random
import prompts
from getpass import getpass

class TerminalInterface:
    
    def __init__(self):
        self.my_dict = {"1": self.write_english, "2": self.write_japanese, "3": self.have_conversation, "4": self.sentence_english, "5": self.sentence_japanese}

    # strat 1
    # fix this by changing NA into None 
    def write_english(self):
        word_bank = self.choose_chapter()
        selected_words = self.choose_quantity(word_bank)
        random.shuffle(selected_words)
        for word in selected_words:
            prompts.convert_to_audio(word[0])
            user_input = input(f"Enter the translation for {word[0]}{', ' if word[1] else ''}{word[1] if word[1] else ''}: ")
            response = prompts.run_program(prompts.llm_prompt_eng, word, user_input)
            if response.answer_correct is False:
                selected_words.append(word)
        
    # strat 2
    def write_japanese(self):
        word_bank = self.choose_chapter()
        selected_words = self.choose_quantity(word_bank)
        random.shuffle(selected_words)
        for word in selected_words:
            # print(word)
            prompts.convert_to_audio(word[3], language="en")
            user_input = input(f"Enter the translation for {word[3]}: ")
            response = prompts.run_program(prompts.llm_prompt_jap, word, user_input)
            if response.answer_correct is False:
                selected_words.append(word)
                
    def sentence_english(self):
        word_bank = self.choose_chapter()
        selected_words = self.choose_quantity(word_bank)
        random.shuffle(selected_words)
        for word in selected_words:
            generated_sentence =  prompts.generate_jp_sentence(word)
            # print(generated_sentence)
            prompts.convert_to_audio(generated_sentence)
            user_input = input(f"The sentence is '{generated_sentence}': ")
            response = prompts.run_program(prompts.llm_prompt_sentence_eng, generated_sentence, user_input)
            if response.answer_correct is False:
                selected_words.append(word)
                
    def sentence_japanese(self):
        word_bank = self.choose_chapter()
        selected_words = self.choose_quantity(word_bank)
        random.shuffle(selected_words)
        for word in selected_words:
            generated_sentence =  prompts.generate_en_sentence(word)
            # print(generated_sentence)
            prompts.convert_to_audio(generated_sentence, language="en")
            user_input = input(f"The sentence is '{generated_sentence}': ")
            response = prompts.run_program(prompts.llm_prompt_sentence_jp, generated_sentence, user_input)
            if response.answer_correct is False:
                selected_words.append(word)
        
    # needs a list that retains the previous sentences, each sentence will be a tuple, first will be who said it, and then the sentence
    # parses these sentences into the prompt llm, 
    def have_conversation(self):
        past_dialogue = []
        word_bank = self.choose_chapter()
        selected_words = self.choose_quantity(word_bank)
        random.shuffle(selected_words)
        for word in selected_words:
            generated_sentence =  prompts.generate_jp_sentence(word) 
            
    
    def run_program(self):
        
        return self.my_dict[self.choice_selection()]()
        
    def home_page(self):
        
        while user_input:=input(
        """
        Welcome to the Japanese learning program!
        1. Login
        2. Signup

        
        """
        ):
            match user_input:
                case "1":
                    return self.login()
                    
                case "2":
                    return self.signup()

                    
        
    def login(self):
        pass
    
    def signup(self):
        pass
    
    def choice_selection(self):
        while (user_input:=input(
            """
Choose from the options below:
1. Translate Japanese to English
2. Translate English to Japanese
3. NA
4. Translate Japanese Sentences to English
5. Translate English Sentences to Japanese

            """)) != "exit":
            return user_input
                
    def choose_chapter(self):
        while (user_input:=input("Choose a chapter number:\n")):
            if user_input == "back":
                return
            
            if user_input == "exit":
                exit()
                
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
            
        # print(word_bank)
        # return word_bank
        return word_bank
        
    # eventually allow all
    def choose_quantity(self, word_bank):
        while (user_input:=input("Choose a quantity:\n")):
            if user_input == "back":
                return
            
            if user_input == "exit":
                exit()
            
            if not user_input.isdigit():
                print("Invalid input. Please enter a number.")
                continue
            
            quantity = int(user_input)
            break
        
        
        if quantity > len(word_bank):
            print(f"Warning: Requested quantity ({quantity}) is greater than the available words ({len(word_bank)}). Using all available words.")
            quantity = len(word_bank)
        
        selected_words = random.sample(word_bank, quantity)
        # print(selected_words)
        return selected_words
    

        
        
        
        