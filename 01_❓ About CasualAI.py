import streamlit as st
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title="Data Import", page_icon=":clipboard:",layout="wide")
st.session_state.update(st.session_state)

add_logo('images/logo.png', height=50)
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

st.subheader("About Casual AI")
