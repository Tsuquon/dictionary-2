from openai import OpenAI
from llm_response_format import LLMResponseFormat
from gtts import gTTS
import os
import pygame

def convert_to_audio(my_text, language='ja'):
    conv_audio = gTTS(text=my_text, lang=language, slow=False)
    audio_file = "tmp_audio/temp.mp3"
    conv_audio.save(audio_file)
    
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()



def run_program(function_name, *args):

    return function_name(*args)

# program gives japanese word, user gives english translation
def llm_prompt_eng(def_word, usr_word):
    # print(usr_word)
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "The format of the tuple is structured as (kana, kanji (opt), pos, definition, chapter number)"},
            {"role": "system", "content": "give your response, followed by boolean if the user provided answer is correct or not"},
            # {"role": "system", "content": f"The given word is {def_word}."},
            {"role": "user", "content": f"My answer is '{usr_word}'. Does this closely match {def_word}?"}
        ],
        response_format=LLMResponseFormat,
        timeout=10
    )
    test = completion.choices[0].message.parsed
    print(test.response)
    print(test.answer_correct)
    return test
    
def llm_prompt_jap(def_word, usr_word):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are going to read the english translation, and the user provides the japanese translation, and see if it matches the translation in the given tuple"},
            {"role": "system", "content": "The format of the tuple is structured as (kana, kanji (opt), pos, definition, chapter number)"},
            {"role": "system", "content": "your response, followed by boolean if it was correct or not"},
            {"role": "system", "content": f"The given tuple is {def_word}."},
            {"role": "user", "content": f"Is the answer in japanese {usr_word}"}
        ],
        response_format=LLMResponseFormat
    )
    test = completion.choices[0].message.parsed
    print(test.response)
    print(test.answer_correct)
    return test

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
    print(test.response)
    print(test.answer_correct)
    return test
    
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
    print(test.response)
    print(test.answer_correct)
    return test
            
            
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

def generate_convo_question(given_word):
    pass