import streamlit as st


def render_sidebar():
    st.set_page_config(initial_sidebar_state="collapsed")
    
    with st.sidebar:
        if st.button("Switch to transcription", use_container_width=True):
            st.switch_page("transcription.py")
        # st.write("yoodayo")

render_sidebar()
pg = st.navigation([st.Page("streamlit/pages/input_chooser.py"), st.Page("streamlit/pages/flash_card.py"), st.Page("streamlit/pages/results.py"), st.Page("streamlit/pages/transcription.py")], position="hidden")
pg.run()

# sider bar