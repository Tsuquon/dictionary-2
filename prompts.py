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

def llm_prompt_eng(def_word, usr_word):
    client = OpenAI()
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are going to read off a tuple giving the kana and kanji (if available, else provide nothing). The user will respond in english, and you will check if the definition matches closely enough to the given translation in the word bank"},
            {"role": "system", "content": "The format of the tuple is structured as (kana, kanji (opt), pos, definition, chapter number)"},
            {"role": "system", "content": "give your response, followed by boolean if the user provided answer is correct or not"},
            {"role": "system", "content": f"The given word is {def_word}."},
            {"role": "user", "content": f"Is the answer in english is {usr_word}"}
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