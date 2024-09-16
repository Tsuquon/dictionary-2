import streamlit as st
import prompts

st.title("Translator")



# # THIS WHOLE THING IS BROKEN

# st.title("Translator")
# word_bank = []

# def get_word_tuple():
#     print("this runs!!")
#     conn = st.connection("postgresql", type="sql")
#     df = conn.query(f"SELECT * FROM dictionary WHERE chapter = {st.session_state.prompt_value[0]}", ttl='10m')
#     random_rows = df.sample(n=int(st.session_state.prompt_value[1]))
#     word_bank = random_rows.values.tolist()
#     yield from word_bank
    

# def store_history():
    
#     # stores chat history
#     if "messages" not in st.session_state:
#         st.session_state.messages = []

#     for message in st.session_state.messages:
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

# def get_chapter():
#     with st.chat_message("ai"):
#         st.markdown("Hey there! Please enter which chapter you'd like to be tested on!")
        
#     if prompt := st.chat_input("Type chapter number"):
#         # Display user message in chat message container
#         with st.chat_message("user"):
#             st.markdown(prompt)
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user","content":prompt})
        
#         if not prompt.isdigit():
#             return
        
#         st.session_state.prompt_value.append(prompt.strip())
#         st.session_state.stage = 1

# def get_quantity():
#     with st.chat_message("ai"):
#         st.markdown("Hey there! Please enter the quantity you'd like to be tested on!")
        
#     if prompt := st.chat_input("Type quantity number"):
#         # Display user message in chat message container
#         with st.chat_message("user"):
        
#             st.markdown(prompt)
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user","content":prompt})
        
#         if not prompt.isdigit():
#             return
        
#         st.session_state.prompt_value.append(prompt.strip())
#         get_word_tuple()
#         st.session_state.stage = 2

# def ask_questions():
#     print("HEY!!!")
#     with st.chat_message("assistant"):
#         try:
#             word = next(get_word_tuple())
#             print(word)
#             st.markdown(f"Enter the translation for {word[0]}{', ' if word[1] else ''}{word[1] if word[1] else ''}: ")
#         except StopIteration:
#             st.markdown("No more words to test.")
#             print("no more words")
#             # return
    
#     if prompt := st.chat_input("Type the translation"):
        
    
#         # Display user message in chat message container
#         with st.chat_message("user"):
#             st.markdown(prompt)
#         # Add user message to chat history
#         st.session_state.messages.append({"role": "user", "content": prompt})
        
        
#         with st.chat_message("assistant"):
#             st.markdown(response:=prompts.run_program(prompts.llm_prompt_eng, word, prompt))
            
#         st.session_state.messages.append({"role": "assistant", "content": response.response})
    
#     # ask_questions()

# def input_interface():
#     print("runs")
    
#     if "prompt_value" not in st.session_state:
#         st.session_state.prompt_value = []
    
#     if "stage" not in st.session_state:
#         st.session_state.stage = 0
    
#     print(st.session_state.stage)
    
#     if st.session_state.stage == 0:
#         get_chapter()
        
#     if st.session_state.stage == 1:
#         get_quantity()
        
#     if st.session_state.stage == 2:
#         # get_word_tuple()
#         ask_questions()
    
# store_history()
# input_interface()