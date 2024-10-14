import streamlit as st


def render_sidebar():
    st.set_page_config(initial_sidebar_state="collapsed")
    
    with st.sidebar:
        if st.button("Switch to transcription", use_container_width=True):
            st.switch_page("transcription.py")
        # st.write("yoodayo")

render_sidebar()
pg = st.navigation([st.Page("input_chooser.py"), st.Page("flash_card.py"), st.Page("results.py"), st.Page("transcription.py")], position="hidden")
pg.run()

# sider bar