# page that will show results at the end of the flash card
# need to store results somewhere

import streamlit as st

# st.write(st.session_state.incorrect_words)

st.title("Results")
st.bar_chart(
    st.session_state.incorrect_words,
    use_container_width=True
)
print(st.session_state.incorrect_words)
col1, col2 = st.columns(2)

with col1:
    if st.button("Return to choosing inputs", use_container_width=True):
        st.switch_page("input_chooser.py")
        
with col2:
    if st.button("Practice wrong words", use_container_width=True):
        st.switch_page("flash_card.py")