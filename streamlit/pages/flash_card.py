# TODO: For the english to japanese, need to send in word[3] or smth instead
# I think the word bank is resetting each time

import itertools
from time import sleep
import streamlit as st
import prompts

st.title("アンケート")
col1, col2 = st.columns(2)
col2.header("答え")
feedback_container = col2.container(height=300)

func_dict = {
    "Japanese to English": prompts.llm_prompt_eng,
    "English to Japanese": prompts.llm_prompt_jap,
}

language_dict = {
    "Japanese to English": "ja",
    "English to Japanese": "en",
}

# @st.cache_resource

def render_box_1():
    col1.header("質問")
    
    # Set up the first word if it's the first render
    # This needs to change sat that it can reset
    if st.session_state.first_render:
        st.session_state.current_word = st.session_state.word_bank[0]
        st.session_state.yield_call = iter(st.session_state.word_bank[1:])
        prompts.convert_to_audio(st.session_state.current_word[0], language=language_dict[st.session_state.translation_type])
        st.session_state.first_render = False

    word = st.session_state.current_word

    message_container = col1.container(height=300).empty()

    with message_container.container():
        print("this runs")
        st.chat_message("ai").write(f"{word[0]}{', ' if word[1] else ''}{word[1] if word[1] else ''}")

    if prompt := col1.chat_input("Type your answer..."):
        # response needs to change dynamically
        response = prompts.run_program(func_dict[st.session_state.translation_type], word, prompt)

        # with message_container.container():
        #     st.chat_message("user").write(prompt)
        render_box_2(response)

        try:
            st.session_state.current_word = next(st.session_state.yield_call)
        except StopIteration:
            st.session_state.current_word = None
            st.session_state.translation_type = None
            st.session_state.selected_chapter = None
            st.session_state.selected_quantity = None
            st.session_state.progress_value = 0
            # Change page to results page instead - or load a button first that when the user is ready goes to results page, or redo, or back to input_chooser.py
            st.switch_page("input_chooser.py")
        else:
            with message_container.container():
                prompts.convert_to_audio(st.session_state.current_word[0], language=language_dict[st.session_state.translation_type])
                st.chat_message("ai").write(f"{st.session_state.current_word[0]}{', ' if st.session_state.current_word[1] else ''}{st.session_state.current_word[1] if st.session_state.current_word[1] else ''}")



        

        # messages.chat_message("ai").write(word)


def render_box_2(response):
    if response.answer_correct:
        feedback_container.chat_message("ai").write("Correct!")
        st.session_state.progress_value += 1

    else:
        feedback_container.chat_message("ai").write("Incorrect!")
        st.session_state.yield_call = itertools.chain(st.session_state.yield_call, iter([st.session_state.current_word]))
    feedback_container.chat_message("ai").write(response.response)
    popover = col2.popover("See usage example")
    popover.write(prompts.get_usage_example(st.session_state.current_word[0]))
    print(st.session_state.word_bank)
def progress_bar():
    if "progress_value" not in st.session_state:
        st.session_state.progress_value = 0
    
    st.progress(st.session_state.progress_value/len(st.session_state.word_bank), text=f"Progress: {st.session_state.progress_value}/{len(st.session_state.word_bank)}")
    

render_box_1()
# st.progress()
    
progress_bar()
    

# render_boxes()
