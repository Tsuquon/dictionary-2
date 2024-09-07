
import random
import pandas as pd
import psycopg2
from database_key import db_host, db_name, db_pass, db_user
from terminal_interface import TerminalInterface


    
    

    
# probably move this into sql setup    



def main():
    interface = TerminalInterface()
    interface.run_program()
    

if __name__ == "__main__":
    main()
    
