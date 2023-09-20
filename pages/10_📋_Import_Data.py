import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_extras.app_logo import add_logo
from streamlit.components.v1 import html

st.set_page_config(page_title="Data Import", page_icon=":clipboard:",layout="wide")
#st.session_state.update(st.session_state)

add_logo('images/logo.png', height=50)
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

st.title("Data Import")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

def clear_session():
    #del st.session_state['csv_file']
    if 'causal_factor_col' in st.session_state:
        del st.session_state['causal_factor_col']
        
    if 'target_outcome_col' in st.session_state:    
        del st.session_state['target_outcome_col']
    
    if 'covariates_cols' in st.session_state:
        del st.session_state['covariates_cols']    

def clearMultiSelect():
    covariates_cols = []
    st.session_state.covariates_cols = []

    if 'causal_factor_col' in st.session_state and 'target_outcome_col' in st.session_state:
        if st.session_state.causal_factor_col == st.session_state.target_outcome_col:
            alert_msg = "<script>alert('Causal Factor cannot be selected same as Target Outcome');</script>"
            html(alert_msg)
            st.session_state.causal_factor_col = df.columns[0]
            st.session_state.target_outcome_col = df.columns[1]

fu = st.file_uploader("Upload a CSV file", type=["csv"])

if fu is not None:
    st.session_state.csv_file = fu      
else:
    st.session_state.csv_file = 'C:\Cardiac-AI\causal\low1.csv'    

           
df = pd.read_csv(st.session_state.csv_file)

# Write the uploaded CSV to server for page sharing
df.to_csv('causal_uploaded_data.csv', index=False, encoding='utf-8')

causal_factor_col = st.selectbox("Select Causal Factor", df.columns)

col_exclude_1 = [col for col in df.columns if col != causal_factor_col]
target_outcome_col = st.selectbox("Select Target Outcome", col_exclude_1)
    
col_exclude_2 = [col for col in col_exclude_1 if col != target_outcome_col]
    
covariates_cols = st.multiselect("Select Covariates", col_exclude_2)


st.session_state.causal_factor_col = causal_factor_col

st.session_state.target_outcome_col = target_outcome_col

st.session_state.covariates_cols = covariates_cols     

# st.write(st.session_state)