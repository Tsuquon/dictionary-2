from time import sleep
import streamlit as st
import prompts

st.title("Translator")
col1, col2 = st.columns(2)
col2.header("Answer")
feedback_container = col2.container(height=300)



# @st.cache_resource

def render_box_1():
    col1.header("Question")
    
    # Set up the first word if it's the first render
    if "first_render" not in st.session_state:
        st.session_state.first_render = True
        st.session_state.current_word = st.session_state.word_bank[0]
        st.session_state.yield_call = iter(st.session_state.word_bank[1:])

    word = st.session_state.current_word

    message_container = col1.container(height=300).empty()

    with message_container.container():
        st.chat_message("ai").write(f"{word[0]}{', ' if word[1] else ''}{word[1] if word[1] else ''}")

    if prompt := col1.chat_input("Type your answer..."):
        response = prompts.run_program(prompts.llm_prompt_eng, word, prompt)

        with message_container.container():
            st.chat_message("user").write(prompt)
            render_box_2(response)

        try:
            st.session_state.current_word = next(st.session_state.yield_call)
        except StopIteration:
            st.session_state.current_word = None
        else:
            with message_container.container():
                st.chat_message("ai").write(f"{st.session_state.current_word[0]}{', ' if st.session_state.current_word[1] else ''}{st.session_state.current_word[1] if st.session_state.current_word[1] else ''}")



        

        # messages.chat_message("ai").write(word)

            


def render_box_2(response):
    feedback_container.chat_message("ai").write(response.response)



render_box_1()
# render_boxes()