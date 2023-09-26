import streamlit as st
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
from streamlit_extras.app_logo import add_logo
import scipy

st.set_page_config(page_title="Causal Factor Model", page_icon=":chart_with_upwards_trend:",layout="wide")
st.session_state.update(st.session_state)

add_logo('images/logo.png', height=50)
st.markdown("""<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

st.title("Causal Factor Model")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# distribution balance chart
# st.write(st.session_state)
# variable_col = st.session_state.causal_factor_col
if 'variable_col' not in st.session_state:
    st.error("Please select the specific variable column in the Summary Statistics Page")
else:
    if st.session_state.variable_col != st.session_state.causal_factor_col:  
        if st.session_state.is_vcol_numeric:
            df = pd.read_csv('causal_uploaded_data.csv')

            c1, c2, c3 = st.columns([49, 2, 49])
            with c1:
                st.markdown('<p style="background-color:#F39C11;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;Raw Data</p>', unsafe_allow_html=True)
                
                styled_df = df.style.apply(
                    lambda x: ['background-color: blue' if colname == st.session_state.causal_factor_col else 'background-color: green' if colname == st.session_state.target_outcome_col else 'background-color: red' if colname == st.session_state.variable_col  else 'background-color: white' for colname in df.columns],
                    axis=1,
                    subset=pd.IndexSlice[:, :]
)                
                #st.dataframe(df)
                st.dataframe(styled_df)
                st.markdown('<span style="background-color: blue; padding: 5px; color: white;">Causal Factor Column</span>', unsafe_allow_html=True)
                st.markdown('<span style="background-color: green; padding: 5px; color: white;">Target Outcome Column</span>', unsafe_allow_html=True)
                st.markdown('<span style="background-color: red; padding: 5px; color: white;">Specific Variable Column</span>', unsafe_allow_html=True)
            with c3:
                st.markdown('<p style="background-color:#F39C11;color:#FFFFFF;font-size:18px;">&nbsp;&nbsp;Distribution Balance of ' + st.session_state.variable_col + '</p>', unsafe_allow_html=True)            
                data1 = df[df[st.session_state.causal_factor_col] == st.session_state.causal_factor_value][st.session_state.variable_col]
                data2 = df[df[st.session_state.causal_factor_col] != st.session_state.causal_factor_value][st.session_state.variable_col]

                if (data1.empty or data2.empty):
                    st.error('Lack of data matching the selected casual factor value')
                else:
                    colors = ['#000000', '#000000']
                    try:
                        fig = ff.create_distplot([data1, data2], ["Data1 (A=1)", "Data2 (A!=1)"], colors=colors, bin_size=10, show_hist=False, show_rug=False)
                        fig.update_traces(marker_line_width=1,marker_line_color="black", showlegend=False)

                        fig.update_layout(width=800, height=600, xaxis_title=st.session_state.variable_col, yaxis_title="Density Within Group",  legend_title= st.session_state.variable_col + ' value when causal factor')

                        x1   = [xc   for xc in fig.data[0].x ]
                        y1   = fig.data[0].y[:len(x1)]

                        x2   = [xc   for xc in fig.data[1].x]
                        y2   = fig.data[1].y[-len(x2):]

                        xc   = [x1   for x1 in fig.data[0].x if x1 in fig.data[1].x]
                        yc   = fig.data[0].y[:len(xc)]

                        fig.add_scatter(x=x2, y=y2,fill='tozeroy', mode='none' , fillcolor='rgba(252,220,218,0.5)', opacity=0.2, name = 'otherwise')
                        fig.add_scatter(x=x1, y=y1,fill='tozeroy', mode='none' , fillcolor='rgba(191,239,241,0.5)', opacity=0.2, name = st.session_state.causal_factor_value)

                        config = {  'displayModeBar': True,
                                    'toImageButtonOptions': {
                                        'filename': 'causal_factor_model',
                                        'height': 1024,
                                        'width': 1280
                                    }
                                }

                        #fig.show()    
                        st.plotly_chart(fig, config=config)
                    except ValueError:
                        st.error('Do not have enought elements to plot the graph')                        
        else:
            st.error('The specific variable is not all numeric')
    else:
        st.error('The specific variable is same as the causal factor')