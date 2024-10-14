# page that will show results at the end of the flash card
# need to store results somewhere

import streamlit as st

# print(st.session_state.incorrect_words)
# st.write(st.session_state.incorrect_words)

st.title("Results")
data = st.session_state.incorrect_words
chart_data = {}

for word in data:
    if word[0] in chart_data:
        chart_data[word[0]] += 1
    else:
        chart_data[word[0]] = 1

st.bar_chart(
    chart_data,
    use_container_width=True
    horizontal=True
)
col1, col2 = st.columns(2)

with col1:
    if st.button("Return to choosing inputs", use_container_width=True):
        st.switch_page("streamlit/pages/input_chooser.py")
        
with col2:
    if st.button("Practice wrong words", use_container_width=True):
        st.switch_page("streamlit/pages/flash_card.py")