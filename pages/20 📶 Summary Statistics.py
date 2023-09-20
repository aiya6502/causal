import streamlit as st
import plotly.express as px
import pandas as pd
from streamlit_extras.app_logo import add_logo
import matplotlib.pyplot as plt
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages
import plotly.io as pio
import pdfkit

st.set_page_config(page_title="Data Import", page_icon=":clipboard:",layout="wide")
st.session_state.update(st.session_state)

add_logo('images/logo.png', height=50)
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

st.title("Summary Statistics")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

c1, c2, c3 = st.columns([49, 2, 49])

st.session_state.csv_file = 'causal_uploaded_data.csv'
with c3:
    st.markdown('<p style="background-color:#F39C11;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;Summary Statistics About A Specific Variable</p>', unsafe_allow_html=True)
    col_list = [st.session_state.causal_factor_col, st.session_state.target_outcome_col] + st.session_state.covariates_cols
    variable_col = st.selectbox('Select a variable', col_list)

if variable_col:
    # Read the CSV file, specifying the column name "V12" and skipping the header row
    df = pd.read_csv(st.session_state.csv_file, usecols=[variable_col])

    # Get the number of rows
    num_rows = df.shape[0]
    missing_values_count = df[variable_col].isnull().sum()

    # Calculate the percentage of missing values
    percentage_missing = round((missing_values_count / num_rows) * 100, 2)

    if percentage_missing.is_integer():
        percentage_string = "{:.0f}%".format(percentage_missing)
    else:
        percentage_string = "{:.2f}%".format(percentage_missing)      

with c1:
    st.markdown('<p style="background-color:#01A65A;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;About the data</p>', unsafe_allow_html=True)
    col_list = [st.session_state.causal_factor_col, st.session_state.target_outcome_col] + st.session_state.covariates_cols
    number_of_covariates = len(col_list)
    summary_df = pd.DataFrame({
        'Statistic': ['Number of covariates', 'Number of subjects', 'Percent of data missing'],
        'Values': [number_of_covariates, num_rows, percentage_string]})
    st.markdown(summary_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)        
    st.markdown('')
c1, c2, c3 = st.columns([49, 2, 49])
with c1:
    st.markdown('<p style="background-color:#F39C11;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;Raw Data</p>', unsafe_allow_html=True)
    raw_df = pd.read_csv(st.session_state.csv_file, usecols=col_list)
    # st.markdown(raw_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    # st.dataframe(raw_df)
    st.write(raw_df)

    csv = raw_df.to_csv(index = False).encode('utf-8')
    st.download_button('Download as CSV', data = csv, file_name = "summary_statistics_raw_data.csv",mime = "text/csv")
    
#    if st.button('Save as PDF'):
#        fig, ax = plt.subplots()
#        ax.axis('tight')
#        ax.axis('off')
#        ax.table(cellText=raw_df.values, colLabels=raw_df.columns, cellLoc='center', loc='center')
#        pp=PdfPages('summary_statistics_raw_data.pdf')
#        pp.savefig(fig, bbox_inches='tight')
#        pp.close()

    
with c3:
    st.markdown('<p style="background-color:#F39C11;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;Distribution of the Variable</p>', unsafe_allow_html=True)
    # st.markdown(f'<h1 style="color:#33ff33;font-size:24px;">{"ColorMeBlue text"}</h1>', unsafe_allow_html=True)
    # st.write(st.session_state)
    
    if variable_col:
        # Read the CSV file, specifying the column name "V12" and skipping the header row
        df = pd.read_csv(st.session_state.csv_file, usecols=[variable_col])


        # Get the number of rows
        num_rows = df.shape[0]
        
      

        # Calculate the minimum, maximum, median, and mean of the column
        min_value = "{:.2f}".format(df.min()[0])
        max_value = "{:.2f}".format(df.max()[0])
        median_value = "{:.2f}".format(df.median()[0])
        mean_value = "{:.2f}".format(df.mean()[0])

        # Create a summary DataFrame
        summary_df = pd.DataFrame({
#            'Number of Rows': [num_rows],
            'Minimum': [min_value],
            'Median': [median_value],
            'Mean': [mean_value],
            'Max': [max_value],
            'Percent Missing': [percentage_string]
        })

        # Display the summary table
        # st.write(summary_df.T)
        #st.write(summary_df)
        st.markdown(summary_df.style.hide(axis="index").to_html(), unsafe_allow_html=True)
        st.markdown('')
        # Display the transposed DataFrame as an HTML table without row numbers
        # html_table = summary_df.T.to_html(index=True, header=False, classes=["dataframe"])
        # st.markdown(html_table, unsafe_allow_html=True)        

    # df = pd.read_csv('C:\Cardiac-AI\causal\low10.csv')
    pd.read_csv(st.session_state.csv_file, usecols=[variable_col])
    # df = px.data.tips()
    # fig = px.histogram(df, x="total_bill", histnorm='probability density')
    fig = px.histogram(df, x=variable_col, histnorm='probability density', color_discrete_sequence=['blue'], nbins=10)
    fig.update_traces(marker_line_width=2,marker_line_color="black")
    #fig.update_layout(xaxis_title=variable_col, yaxis_title="Density", title='Distribution of ' + variable_col,margin=dict(l=10, r=10, t=30, b=10), title_x=0.1, title_font=dict(family="Arial", size=12))
    fig.update_layout(xaxis_title=variable_col, yaxis_title="Density", title='Distribution of ' + variable_col)
    #config = {'displayModeBar': True}
    config = {
        'toImageButtonOptions': {
            'format': 'jpeg', # one of png, svg, jpeg, webp
            'filename': 'density_histogram',
            'height': 768,
            'width': 1024,
            'scale': 1 # Multiply title/legend/axis/canvas sizes by this factor
            },
        'displayModeBar': True,
        'displaylogo': False
        }
    #fig.show()    
    st.plotly_chart(fig, config=config)
    
    if st.button('Save'):
        fig.write_image('test123.png')
        pio.write_image(fig, "test123..pdf")
