import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_extras.app_logo import add_logo
from streamlit.components.v1 import html

st.set_page_config(page_title="Data Import", page_icon=":clipboard:",layout="wide")
#st.session_state.update(st.session_state)

add_logo('images/logo.png', height=50)
st.markdown("""<style> .reportview-container {margin-top: -2em;} #MainMenu {visibility: hidden;} .stDeployButton{display: none;} #stDecoration {display: none;}  footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

st.title("Data Import")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

select_default = 'Please choose...'

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
#fu = 'low1.csv'
if fu is None:
    st.error('Select a CSV file first')
else:
    st.session_state.csv_file = fu

    df = pd.read_csv(st.session_state.csv_file)
    # Get the row count and column count
    row_count = df.shape[0]
    column_count = df.shape[1]

    # Check the conditions for rejecting the file, if rejected, read the default file instead
    if row_count < 2 or column_count < 3:
        st.error("Rejected: The CSV file must have at least 2 rows and 3 columns. Please upload another file")
    else:    
        # Write the uploaded CSV to server for page sharing
        df.to_csv('causal_uploaded_data.csv', index=False, encoding='utf-8')
        
        options_1 = [select_default] + df.columns.tolist()
        causal_factor_col = st.selectbox("Select Causal Factor", options_1)
        
        if causal_factor_col != select_default:
            options_2 = [select_default] + sorted(df[causal_factor_col].unique().tolist())
            causal_factor_value = st.selectbox("Select target Causal Factor value", options_2)
            
            if causal_factor_value != select_default:
                options_3 = [col for col in options_1 if col != causal_factor_col]
                target_outcome_col = st.selectbox("Select Target Outcome", options_3)
                
                if target_outcome_col != select_default:                
                    options_4 = [select_default] + sorted(df[target_outcome_col].unique().tolist())
                    target_outcome_value = st.selectbox("Select target Outcome value", options_4)
                        
                    col_exclude_2 = [col for col in options_3 if col != target_outcome_col]
                        
                    covariates_cols = st.multiselect("Select Covariates", col_exclude_2)


                    st.session_state.causal_factor_col = causal_factor_col
                    st.session_state.causal_factor_value = causal_factor_value
                    
                    st.session_state.target_outcome_col = target_outcome_col
                    st.session_state.target_outcome_value= target_outcome_value
                    
                    st.session_state.covariates_cols = covariates_cols    
                    st.session_state.b_size = 10
