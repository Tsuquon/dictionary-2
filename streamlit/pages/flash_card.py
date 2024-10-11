import itertools
from time import sleep
import streamlit as st
import prompts
import random

if "audio_toggle" not in st.session_state:
    st.session_state.audio_toggle = True

# Move this into col 1
with st.container():
    upcol_1, upcol_2 = st.columns([0.2, 0.8])
    with upcol_1:
        upcol_1_1, upcol_1_2 = st.columns(2)
        with upcol_1_1:
            if st.button(":material/arrow_back:"):
                st.switch_page("input_chooser.py")
                
        with upcol_1_2:
            with st.popover(":material/settings:"):
                st.session_state.audio_toggle = st.toggle("Audio", value = st.session_state.audio_toggle)

if 'incorrect_words' not in st.session_state:
    st.session_state.incorrect_words = {}

if 'my_option' not in st.session_state:
    st.session_state.my_option = ""
    
st.title("アンケート")
col1, col2 = st.columns(2)
col2.header("前の回答")
feedback_container = col2.container(height=300)

func_dict = {
    "Japanese to English": prompts.llm_prompt_eng,
    "English to Japanese": prompts.llm_prompt_jap,
}

language_dict = {
    "Japanese to English": "ja",
    "English to Japanese": "en",
}

word_num_dict = {
    "Japanese to English": 0,
    "English to Japanese": 3,
}

word_num_dict_same = {
    "Japanese to English": (3,),
    "English to Japanese": (0,1)
}

verb_classification = ('u-v.','ru-v.','irr-v.')
adjective__classification = ('い-adj.','な-adj.')

def option_selection(word):
    options = st.session_state.testing_options
    option_selection = ""
    option0 = random.choice(options[0])
    option1 = random.choice(options[1])
    option2 = random.choice(options[2])
    
    if word[2] in adjective__classification:
        option_selection = f"{option1}, {option2}"
    
    elif word[2] in verb_classification and option0 == 'te':    
        option_selection = f"{option0}, {option2}"
    
    elif word[2] in verb_classification:
        option_selection = f"{option0}, {option1}, {option2}"
    
    return option_selection

# @st.cache_resource
def render_box_1():
    col1.header("現在質問")
    
    # Set up the first word if it's the first render
    # This needs to change sat that it can reset
    if st.session_state.first_render:
        st.session_state.current_word = st.session_state.word_bank[0]
        st.session_state.yield_call = iter(st.session_state.word_bank[1:])
        st.session_state.my_option = option_selection(st.session_state.current_word)

        if st.session_state.audio_toggle:
            prompts.convert_to_audio(st.session_state.current_word[word_num_dict[st.session_state.translation_type]], language=language_dict[st.session_state.translation_type])
        st.session_state.first_render = False

    word = st.session_state.current_word

    message_container = col1.container(height=300).empty()

    with message_container.container():
        st.chat_message("ai").write(f"{word[word_num_dict[st.session_state.translation_type]]}{', ' if word[1] and st.session_state.translation_type == 'Japanese to English' else ''}{word[1] if word[1] and st.session_state.translation_type == 'Japanese to English' else ''}")
        # check if verb first

        

        # Put this next to the input box
        if st.button("Replay Audio"):
            if st.session_state.audio_toggle:
                prompts.convert_to_audio(st.session_state.current_word[word_num_dict[st.session_state.translation_type]], language=language_dict[st.session_state.translation_type])
                

    if prompt := col1.chat_input("答えて下さい。。。"):
        # response needs to change dynamically

        my_options = st.session_state.my_option.split(", ")
        
        if (prompt in [word[x] for x in word_num_dict_same[st.session_state.translation_type]] 
            and ((word[2] not in verb_classification and word[2] not in adjective__classification) 
                 or (my_options[0] == "casual" and my_options[1] == "present" and my_options[2] == "affirmative"))):
            class Response:
                def __init__(self, answer_correct, response):
                    self.answer_correct = answer_correct
                    self.response = response

            response = Response(
                answer_correct=True,
                response=f"'{prompt}' is correct for '{word}'"
            )
            render_box_2(response)
        
        else:    
            # te verb exception, since it can't have a tense
            response = prompts.run_program(func_dict[st.session_state.translation_type], word, prompt, st.session_state.my_option)
            # print(word, prompt)
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
            st.switch_page("results.py")
        else:
            with message_container.container():
                if st.session_state.audio_toggle:
                    prompts.convert_to_audio(st.session_state.current_word[word_num_dict[st.session_state.translation_type]], language=language_dict[st.session_state.translation_type])
                st.chat_message("ai").write(f"{st.session_state.current_word[word_num_dict[st.session_state.translation_type]]}{', ' if st.session_state.current_word[1] and st.session_state.translation_type == 'Japanese to English' else ''}{st.session_state.current_word[1] if st.session_state.current_word[1] and st.session_state.translation_type == 'Japanese to English' else ''}")
                st.session_state.my_option = option_selection(st.session_state.current_word)        
                # if st.session_state.my_option != "":
                # Maybe move this upwards, because first word doesnt render the types
                st.chat_message("ai").write(f"{st.session_state.my_option}")
        

        # messages.chat_message("ai").write(word)

def render_box_2(response):
    if response.answer_correct:
        prompts.play_audio("tmp_audio/correct-sound.mp3")
        feedback_container.chat_message("ai").write("Correct!")
        st.session_state.progress_value += 1
    else:
        feedback_container.chat_message("ai").write("Incorrect!")
        st.session_state.yield_call = itertools.chain(st.session_state.yield_call, iter([st.session_state.current_word]))
        
        word = st.session_state.current_word[0]
        if word in st.session_state.incorrect_words:
            st.session_state.incorrect_words[word] += 1
        else:
            st.session_state.incorrect_words[word] = 1

    feedback_container.chat_message("ai").write(response.response)
    popover = col2.popover("See usage example")
    popover.write(prompts.get_usage_example(st.session_state.current_word[0]))

def progress_bar():
    if "progress_value" not in st.session_state:
        st.session_state.progress_value = 0
    
    st.progress(st.session_state.progress_value/len(st.session_state.word_bank), text=f"Progress: {st.session_state.progress_value}/{len(st.session_state.word_bank)}")



render_box_1()  
progress_bar()
