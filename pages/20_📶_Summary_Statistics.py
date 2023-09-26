import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from streamlit_extras.app_logo import add_logo
import scipy

st.set_page_config(page_title="Summary Statistics", page_icon=":clipboard:",layout="wide")
st.session_state.update(st.session_state)

add_logo('images/logo.png', height=50)
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

def get_percentage(p):
    if p.is_integer():
        percentage_string = "{:.0f}%".format(p)
    else:
        percentage_string = "{:.2f}%".format(p)      
    return percentage_string

def is_categorical(x, c):
    binary_cols = [col for col in x.columns if x[col].nunique() == 2]
    categorical_cols_dtype = x.select_dtypes(include=['object']).columns.tolist()
    threshold = 0.01 * len(x)
    categorical_cols_unique = [col for col in x.columns if x[col].nunique() < threshold]

	# Merging lists and removing duplicates
    categorical_cols = list(set(categorical_cols_dtype + categorical_cols_unique))
    categorical_cols = [col for col in categorical_cols if col not in binary_cols]

    if c in categorical_cols:
        return True
    else:
        return False

if 'causal_factor_col' not in st.session_state:
    st.error("Please select co-variates in the Import Data Page")
else:    
    st.title("Summary Statistics")
    st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

    c1, c2, c3 = st.columns([49, 2, 49])

    st.session_state.csv_file = 'causal_uploaded_data.csv'
    st.session_state.is_vcol_numeric = False
    df = pd.read_csv(st.session_state.csv_file)
    with c3:
        st.markdown('<p style="background-color:#F39C11;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;Summary Statistics About A Specific Variable</p>', unsafe_allow_html=True)
        col_list = sorted(df.columns.tolist())
        variable_col = st.selectbox('Select a variable', col_list)

        if variable_col:
            # Get the number of rows
            num_rows = df.shape[0]
            missing_values_count = df[variable_col].isnull().sum()

            # Calculate the percentage of missing values
            data_missing_percentage = get_percentage(round((missing_values_count / num_rows) * 100, 2))

            # Calculate the percentage of rows equal to target causal value
            target_causal_value_rows = len(df[df[st.session_state.causal_factor_col] == st.session_state.causal_factor_value])
            target_causal_value_percentage = get_percentage(round((target_causal_value_rows / num_rows) * 100, 2))
            
            # Calculate the percentage of rows equal to target outcome
            target_outcome_value_rows = len(df[df[st.session_state.target_outcome_col] == st.session_state.target_outcome_value])
            target_outcome_percentage = get_percentage(round((target_outcome_value_rows / num_rows) * 100, 2))
            
            st.session_state.variable_col = variable_col

            check_1 = False
            check_2 = True
            
            if is_categorical(df, variable_col):
                check_1 = True
                check_2 = False

            st.checkbox('Categorical', value=check_1, disabled=True)
            st.checkbox('Not Categorical', value=check_2, disabled=True)
        
    with c1:
        st.markdown('<p style="background-color:#01A65A;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;About the data</p>', unsafe_allow_html=True)

        number_of_covariates = len(col_list) - 2
        summary_df = pd.DataFrame({
            'Statistic': ['Number of covariates', 'Number of subjects', 'Percent of data missing', 'Percent with target causal value', 'Percent with targetg outcome'],
            'Values': [number_of_covariates, num_rows, data_missing_percentage, target_causal_value_percentage, target_outcome_percentage]})
        st.markdown(summary_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)        
        st.markdown('')
        
    c1, c2, c3 = st.columns([49, 2, 49])
    with c1:
        st.markdown('<p style="background-color:#F39C11;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;Raw Data</p>', unsafe_allow_html=True)
        st.dataframe(df)

        csv = df.to_csv(index = False).encode('utf-8')
        st.download_button('Download as CSV', data = csv, file_name = "summary_statistics_raw_data.csv",mime = "text/csv")
        
    with c3:
        st.markdown('<p style="background-color:#F39C11;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;Distribution of the Variable</p>', unsafe_allow_html=True)
        
        if variable_col:
            # df = pd.read_csv(st.session_state.csv_file, usecols=[variable_col])

            # Get the number of rows
            df_vcol = df[variable_col]    
            num_rows = df_vcol.shape[0]

            # Check if the variable column numeric
            try:
                numeric_column = pd.to_numeric(df_vcol)
                is_vcol_numeric = True
            except (ValueError, TypeError):
                is_vcol_numeric = False
        
            if is_vcol_numeric:
                # Calculate the minimum, maximum, median, and mean of the column
                min_value = "{:.2f}".format(df_vcol.min())
                max_value = "{:.2f}".format(df_vcol.max())
                median_value = "{:.2f}".format(df_vcol.median())
                mean_value = "{:.2f}".format(df_vcol.mean())

                # Create a summary DataFrame
                summary_df = pd.DataFrame({
        #            'Number of Rows': [num_rows],
                    'Minimum': [min_value],
                    'Median': [median_value],
                    'Mean': [mean_value],
                    'Max': [max_value],
                    'Percent Missing': [data_missing_percentage]
                })

                st.markdown(summary_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                st.markdown('')

                if 'b_size' not in st.session_state:
                    hb_size = 10
                else:
                    hb_size = st.session_state.b_size
                    
                group_labels = [f'{variable_col}']
                colors = ['#6594EC']
                fig = ff.create_distplot([df[variable_col]], group_labels, colors=colors,
                                     bin_size=hb_size, show_rug=False)
                fig.update_traces(marker_line_width=2,marker_line_color="black", showlegend=False)
                fig.update_layout(xaxis_title=variable_col, yaxis_title="Density", title='Distribution of ' + variable_col)
                
                config = {  'displayModeBar': True,
                            'toImageButtonOptions': {
                                'filename': 'distribution_plot',
                                'height': 1024,
                                'width': 1280
                            }
                        }

                st.plotly_chart(fig, config=config)
                
                b_size = st.slider('Adjust Histogram Bin Width', 0, 50, 10)
                st.session_state.b_size = b_size
                st.session_state.is_vcol_numeric = True

