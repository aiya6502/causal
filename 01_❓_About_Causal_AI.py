import streamlit as st
from streamlit_extras.app_logo import add_logo

st.set_page_config(page_title="About Causal AI", page_icon=":question:",layout="wide")
st.session_state.update(st.session_state)

add_logo('images/logo.png', height=50)
st.markdown("""<style> .reportview-container {margin-top: -2em;} #MainMenu {visibility: hidden;} .stDeployButton{display: none;} #stDecoration {display: none;}  footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

st.subheader("About Casual AI")
