from openai import OpenAI
from llm_response_format import LLMResponseFormat, ConversationResponse
from gtts import gTTS
import st
import pygame

def play_audio(audio_file, volume=0.2):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play()
    except Exception as e:
        print(e)
        st.warning("Error playing audio - streamlit doesn't natively support audio playback without the player. Will find a workaround soon :)") 
        

# this is google's api for simple text to speech
def convert_to_audio(my_text, language='ja'):
    conv_audio = gTTS(text=my_text, lang=language, slow=False)
    audio_file = "tmp_audio/temp.mp3"
    conv_audio.save(audio_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play()

# open ai model for tts
def text_to_speech(text):
    audio_file = "tmp_audio/tts_speech.mp3"
    client = OpenAI()
    completion = client.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
        input=text
    )
    
    completion.stream_to_file(audio_file)

def speech_to_text(audio_file):
    client = OpenAI()
    completion = client.audio.transcriptions.create(
        model="whisper-1",
        file=audio_file
    )
    return completion.text

def run_program(function_name, *args):

    return function_name(*args)

# program gives japanese word, user gives english translation
def llm_prompt_eng(def_word, usr_word, custom_arguments=""):
    # print(usr_word)
    client = OpenAI()
    if custom_arguments != "":
        custom_arguments = "and is " + custom_arguments
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "The format of the tuple is structured as (kana, kanji (opt), pos, definition, chapter number)"},
            {"role": "system", "content": "give your response, followed by boolean if the user provided answer is correct or not"},
            {"role": "user", "content": f"My answer is '{usr_word}'. Does this closely match {def_word}?"}
        ],
        response_format=LLMResponseFormat,
        timeout=10
    )
    test = completion.choices[0].message.parsed
    # print(test.response)
    # print(test.answer_correct)
    return test
    
# program gives the english translation, user gives japanese translation
def llm_prompt_jap(def_word, usr_word, custom_arguments=""):
    client = OpenAI()
    custom_arguments_str = f" and is in the form {custom_arguments}" if custom_arguments else ""
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are evaluating a Japanese translation. The English word or phrase is from the following tuple: {def_word}. The user's Japanese translation should be correct{custom_arguments_str}."},
            {"role": "user", "content": f"Is '{usr_word}' the correct Japanese translation{custom_arguments_str}? Respond in English with your evaluation and explanation."}
        ],
        response_format=LLMResponseFormat
    )
    return completion.choices[0].message.parsed
# not used
# given a chapter number, choose any words from here and below and make a sentence in japanese, the user will have to translate into english
def llm_prompt_sentence_eng(given_sentence, user_trans):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[

            {"role": "system", "content": f"The given sentence in japanese is {given_sentence}."},
            {"role": "user", "content": f"Is '{user_trans}' an accurate translation of '{given_sentence}'?"}
        ],
        response_format=LLMResponseFormat,
        timeout=10
    )
    test = completion.choices[0].message.parsed
    # print(test.response)
    # print(test.answer_correct)
    return test
    
# not used
def generate_jp_sentence(given_word):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You will return just a japanese sentence, and after in brackets, the romaji"},
            {"role": "user", "content": f"The given word is {given_word}. Generate a simple sentence using this word"}
        ],
        timeout=10
    )
    test = completion.choices[0].message.content
    return test

# not used
def llm_prompt_sentence_jp(given_sentence, user_trans):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[

            {"role": "system", "content": f"The given sentence in English is {given_sentence}."},
            {"role": "system", "content": f"After each answer, provide your given correct translation, alongside romaji"},
            {"role": "user", "content": f"Is '{user_trans}' an accurate translation of '{given_sentence}'?"}
        ],
        response_format=LLMResponseFormat,
        timeout=10
    )
    test = completion.choices[0].message.parsed
    # move this into terminal_interface.py
    # print(test.response)
    # print(test.answer_correct)
    return test         

#not used
def generate_en_sentence(given_word):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You will return just an english sentence"},
            {"role": "user", "content": f"The given Japanese word is {given_word}. Generate a simple english sentence using this word"}
        ]
    )
    test = completion.choices[0].message.content
    return test

def get_usage_example(given_word):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": f"Return a japanese sentence using the given word {given_word}, then in parenthesis, the romaji. Then the english translation"},
        ],
        timeout=10
    )
    test = completion.choices[0].message.content
    return test


# in beta
def generate_conversation(vocab_list, total_response=None):
    client = OpenAI()
    messages = [
        {"role": "system", "content": f"Ask a conversational starter question in Japanese using this vocabulary list: {vocab_list}"}
    ]

    if total_response is None:
        messages.append({"role": "user", "content": "Start the conversation"})
    else:
        messages.extend(total_response)

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        timeout=10
    )
    return completion.choices[0].message.content

def feedback_generator(ai_response, user_response):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You will provide feedback on the user's response, only checking correctness of the response. Do not provide any additional information"},
            {"role": "user", "content": f"The given ai question is '{ai_response}', the user responds with '{user_response}'. Provide feedback on the user's response in English"}
        ],
        timeout=10,
        response_format=LLMResponseFormat
    )
    test = completion.choices[0].message.parsed
    return test

