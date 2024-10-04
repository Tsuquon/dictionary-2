import streamlit as st

# Needs quantity, chapter, and type of translation mode

st.title("Customise Input")



# eventually cache this data - also cache this connection
# @st.cache_data
# @st.cache_resource
def get_quantity_from_db(chapter_number):
    import random

    conn = st.connection("postgresql", type="sql")
    
    
    st.session_state.word_bank = conn.query(f"SELECT * FROM dictionary WHERE chapter = {chapter_number}", ttl='10m').values.tolist()
    random.shuffle(st.session_state.word_bank)
    return len(st.session_state.word_bank)

def translation_mode():
    
    translation_type = st.selectbox(
        "Select translation type",
        ("Japanese to English", "English to Japanese"),
        index=0,
        placeholder="Select translation type",
        
    )
    
    return translation_type

def testing_options(translation_type):
    if translation_type == "Japanese to English":
        verb_options = st.multiselect(
            "Select verb options",
            ["casual"],
            ["casual"],
            placeholder="defaults to casual"
        )
        
        tense_options = st.multiselect(
            "Select adjective options",
            ["present"],
            ["present"],
            placeholder="defaults to present"
        )
        
        happen_form = st.multiselect(
            "Select tense options",
            ["affirmative"],
            ["affirmative"],
            placeholder="defaults to affirmative"
        )
    else:
        # should only apply for verbs and adjectives 
        verb_options = st.multiselect(
            "Select verb options",
            ["te", "polite", "casual"],
            ["casual"],
            placeholder="defaults to casual"
        )
        
        tense_options = st.multiselect(
            "Select adjective options",
            ["present", "past"],
            ["present"],
            placeholder="defaults to present"
        )
        
        happen_form = st.multiselect(
            "Select tense options",
            ["affirmative", "negative"],
            ["affirmative"],
            placeholder="defaults to affirmative"
        )
    
    # applies to only verbs
    if verb_options is None:
        verb_options = ["casual"]
    
    # applies to verbs and adjectives
    if tense_options is None:
        tense_options = ["present"]
        
    # applies to verbs and adjectives
    if happen_form is None:
        happen_form = ["affirmative"]
        
    return verb_options, tense_options, happen_form

# This updates whenever chapter updates - should return the number of words from a chapter
def chapter():
    chapter = st.slider(
        "Select chapter",
        min_value=0,
        max_value=12,
        value=0,
        step=1,
    )
    return chapter

def quantity(word_value=0):
    quantity = st.slider(
        "Select quantity",
        min_value=0,
        max_value=word_value,
        value=0,
        step=1,
        
    )
    st.session_state.word_bank = st.session_state.word_bank[:quantity]
    return quantity

def render_button():
    if st.button("Submit"):
        if st.session_state.translation_type == "" or st.session_state.selected_quantity == 0:
            st.write("Please select a translation type and quantity.")
        else:
            st.session_state.first_render = True
            
            if "progress_value" in st.session_state:
                st.session_state.progress_value = 0
        # st.write("Button clicked!")
            print(st.session_state.testing_options)
            st.switch_page("flash_card.py")

# session state definitions
if "translation_type" not in st.session_state:
    st.session_state.translation_type = ""

if "word_bank" not in st.session_state:
    st.session_state.word_bank = []
    
if "selected_chapter" not in st.session_state:
    st.session_state.selected_chapter = 0
    
if "selected_quantity" not in st.session_state:
    st.session_state.selected_quantity = 0
    
if "testing_options" not in st.session_state:
    st.session_state.testing_options = None



# main runnings
selected_translation = translation_mode()
selected_options = testing_options(selected_translation)
selected_chapter = chapter()
selected_quantity = quantity(get_quantity_from_db(selected_chapter))

# sesstion state application
st.session_state.translation_type = selected_translation
st.session_state.testing_options = selected_options
st.session_state.selected_chapter = selected_chapter
st.session_state.selected_quantity = selected_quantity

render_button()

