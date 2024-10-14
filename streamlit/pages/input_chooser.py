import streamlit as st

st.title("Customise Input")

# In the future, extract out the assignment word bank from here
def get_quantity_from_db(chapter_numbers, selected_pos):
    import random

    conn = st.connection("postgresql", type="sql")
    
    pos_condition = " OR ".join([f"pos = '{pos}'" for pos in selected_pos])
    chapter_condition = " OR ".join([f"chapter = {chapter}" for chapter in chapter_numbers])
    query = f"SELECT * FROM dictionary WHERE ({chapter_condition}) AND ({pos_condition})"
    
    st.session_state.word_bank = conn.query(query, ttl='10m').values.tolist()
    random.shuffle(st.session_state.word_bank)
    return len(st.session_state.word_bank)

def translation_mode():
    
    translation_type = st.selectbox(
        "Select translation type",
        ("Japanese to English", "English to Japanese", "Conversation Mode"),
        index=0,
        placeholder="Select translation type",
        
    )
    
    return translation_type

def word_types():
    all_options = []
    
    col1, col2, col3 = st.columns(3)
    with col1:
        quick_select_verb = st.checkbox("Quick select verb", value=True)
    with col2:
        quick_select_adjectives = st.checkbox("Quick select adjectives", value=True)
    with col3:
        quick_select_other = st.checkbox("Quick select other", value=True)
    
    if quick_select_verb:
        all_options.extend(["u-v.", "ru-v.", "irr-v."])
    
    if quick_select_adjectives:
        all_options.extend(["い-adj.", "な-adj."])
    
    if quick_select_other:
        all_options.extend(["pre.", "n.", "exp.", "part.", "suf.", "adv."])

    word_options = st.multiselect(
        "Select word options",
        ("pre.", "n.", "い-adj.", "u-v.", "exp.", "part.", "suf.", "adv.", "な-adj.", "irr-v.", "ru-v."),
        default=all_options,
        placeholder="defaults to all"
    )    
    if not word_options:
        word_options = ["pre.", "n.", "い-adj.", "u-v.", "exp.", "part.", "suf.", "adv.", "な-adj.", "irr-v.", "ru-v."]

    return word_options

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
    elif translation_type == "English to Japanese":
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
    chapter_quick_select = st.checkbox("Quick select all chapters")
    
    my_default = list(range(13))
    
    chapters = st.multiselect(
        "Select chapters",
        options=list(range(13)),
        default=my_default if chapter_quick_select else None,
        placeholder="Defaults to all chapters"
    )
    if chapters == []:
        chapters = list(range(13))
    
    return chapters

def quantity(word_value=0):
    try:
        quantity = st.slider(
            "Select quantity",
            min_value=0,
            max_value=word_value,
            value=0,
            step=1,
            
        )
    except(st.errors.StreamlitAPIException):
        st.error("Chosen requisites have 0 words available")
        quantity = 0
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
            st.switch_page("streamlit/pages/flash_card.py")
            
def alternate_render_button():
    if st.button("Submit"):
        if st.session_state.selected_chapters[0] > st.session_state.selected_chapters[1]:
            st.error("Lower chapter number must be lower than higher chapter number")
        else:
            st.session_state.dialogue = []
            st.switch_page("streamlit/pages/transcription.py")

# session state definitions
if "translation_type" not in st.session_state:
    st.session_state.translation_type = ""

if "word_bank" not in st.session_state:
    st.session_state.word_bank = []
    
if "selected_chapters" not in st.session_state:
    st.session_state.selected_chapters = [0]
    
if "selected_quantity" not in st.session_state:
    st.session_state.selected_quantity = 0
    
if "testing_options" not in st.session_state:
    st.session_state.testing_options = None

def alternate_chapter():
    low = st.number_input("Select the lower chapter number", min_value=0, max_value=12, value=0, step=1)
    high = st.number_input("Select the higher chapter number", min_value=0, max_value=12, value=0, step=1)
    return (low, high)
    
# main runnings
selected_translation = translation_mode()

if selected_translation == "Conversation Mode":
    selected_chapters = alternate_chapter()
    st.session_state.selected_chapters = selected_chapters
    alternate_render_button()
    
else:
    
    
    selected_pos = word_types()
    selected_options = testing_options(selected_translation)
    selected_chapters = chapter()
    selected_quantity = quantity(get_quantity_from_db(selected_chapters, selected_pos))

    # sesstion state application
    st.session_state.translation_type = selected_translation
    st.session_state.testing_options = selected_options
    st.session_state.selected_chapters = selected_chapters
    st.session_state.selected_quantity = selected_quantity

    render_button()
