import streamlit as st


def render_sidebar():
    st.set_page_config(initial_sidebar_state="collapsed")
    
    with st.sidebar:
        st.write("yoodayo")

render_sidebar()
pg = st.navigation([st.Page("input_chooser.py"), st.Page("flash_card.py"), st.Page("results.py")], position="hidden")
pg.run()

# sider bar