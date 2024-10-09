from prompts import generate_conversation, feedback_generator, text_to_speech, play_audio
# import prompts
from database_key import db_host, db_name, db_pass, db_user
import psycopg2
import streamlit as st
import time

def extract_words(chapter_number):
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
        SELECT kana, kanji, translation
        FROM dictionary
        WHERE chapter BETWEEN %s AND %s
        ORDER BY RANDOM();
    """
    
    with conn.cursor() as curs:
        curs.execute(sql, chapter_number)
        results = curs.fetchall()
        
    conn.close()
    
    return results

# dialogue = []

def run_test(chapter_number, user_response=None, initial=False):
    if initial:
        words = extract_words(chapter_number)
        # this needs to change to generalised version
        response = generate_conversation(words)
        st.session_state.dialogue.extend([
            {"role": "user", "content": "Generate a question/response"},
            {"role": "assistant", "content": response}
        ])
    else:
        st.session_state.dialogue.append({"role": "user", "content": user_response})
        words = extract_words(chapter_number)
        response = generate_conversation(words, st.session_state.dialogue)
        st.session_state.dialogue.append({"role": "assistant", "content": response})
    
    # print(response)
    return response

# -----------------------------------------------------------------------------
# main runnings begin here
# -----------------------------------------------------------------------------


col1, col2 = st.columns(2)

message_container = col1.container(height=500, border=True)
feedback_container = col2.container(height=500, border=True)

if "dialogue" not in st.session_state:
    st.session_state.dialogue = []
    response = run_test(st.session_state.selected_chapters, initial=True)
    with message_container:
        st.chat_message("ai").write(response)
        text_to_speech(response)
        play_audio("tmp_audio/tts_speech.mp3")
        


def generate_container():
    chat_input = st.chat_input("Enter response: ")
    with message_container:
        if chat_input:
            run_test(st.session_state.selected_chapters, user_response=chat_input)
            for message in st.session_state.dialogue[1:]:
                if message["role"] == "assistant":
                    messenger = "ai"
                else:
                    messenger = "user"
                
                with st.chat_message(messenger):
                    st.write(message["content"])
                    time.sleep(0.1)
            
            text_to_speech(st.session_state.dialogue[-1]["content"])
            play_audio("tmp_audio/tts_speech.mp3")

            with feedback_container:
                # Check this statement
                # st.write(st.session_state.dialogue[-3]["content"], chat_input)
                feedback = feedback_generator(st.session_state.dialogue[-3]["content"], chat_input)
                st.write(feedback.response)
                    


generate_container()

# for individual testing
if __name__ == "__main__":
    print(run_test(initial=True))
    
    while True:
        user_input = input("Enter response: ")
        run_test(user_response=user_input)
