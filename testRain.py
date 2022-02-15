from importlib.resources import path
from nbformat import write
import pandas as pd
import numpy as np
import streamlit as st

import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.graph_objs import *
import plotly.express as px

from pathlib import Path
import base64

# Initial page config

st.set_page_config(
     page_title='Streamlit India Rainfall Analysis',
     layout="wide",
     page_icon="🧊",
     initial_sidebar_state="expanded",
)

def img_to_bytes(img_path):
    #to encode an image into a string
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

st.sidebar.markdown('''[<img src='data:image/png;base64,{}' class='img-fluid' width=150 height=85>](https://www.aub.edu.lb/)'''.format(img_to_bytes("AUB.png")), 
                    unsafe_allow_html=True)

st.sidebar.header('Streamlit India Rainfall Analysis')

st.sidebar.markdown('''
<small>This [Dataset](https://www.kaggle.com/saisaran2/rainfall-data-from-1901-to-2017-for-india), was taken from [Kaggle](https://www.kaggle.com/).</small>
    ''', unsafe_allow_html=True)

st.sidebar.markdown('__Dataset Preview__')

st.sidebar.code('Welcome To My Streamlit App')


header = st.container()
with header:
   st.write(""" # Rainfall Analysis in India :droplet: 
   In this project, I look into rainfall amounts across different cities in india over different months since 1901 till 2017.""")

path_csv = 'C:\\Users\\Amir\\Desktop\\Rainfall_data\\Rainfall_Data_LL.csv'

def load_csv(path):
    df = pd.read_csv(path)
    return df

data_load_state = st.text('Loading data...')
df = load_csv(path_csv)
data_load_state.text("Done!")

#Create season features
df['Q1'] = df['DEC']+df['JAN']+df['FEB']
df['Q2'] = df['MAR']+df['APR']+df['MAY']
df['Q3'] = df['JUN']+df['JUL']+df['AUG']
df['Q4'] = df['SEP']+ df['OCT']+df['NOV']

#Drop unneccesary columns
to_drop = ['Jan-Feb','Mar-May','June-September', 'Oct-Dec']
df.drop(to_drop, axis=1, inplace=True )

#Rename Columns
df=df.rename(columns={"Name":"Index","SUBDIVISION": "Regions"})

df.columns = df.columns.str.capitalize()

#Create monthly average rain amount 
df["Month Average"] = df['Annual']/12

shape = df.shape
columns = df.columns

regions_number = df['Regions'].nunique() #36 unique region 
no_year = df['Year'].nunique() #117 year
final_year = df['Year'].max() #2017
start_year = df['Year'].min() #1901


with header:
    st.header('India Rainfall Dataset')
    data_bool = st.sidebar.checkbox("Show Dataset Specifications")

    if st.checkbox('Show raw data'):
        st.subheader('Raw data')
        st.write(df)

    if data_bool:
        st.write('Shape of dataset : ', shape)
        st.write('Number of Regions : ', regions_number)
        st.write('Number of years : ', no_year)
        st.write('First year recorded : ',start_year)
        st.write('Last year recorded : ',final_year)
        st.write('Fields of the data is below,', df.columns)


RegionList = df.groupby('Regions').count().index

st.markdown("### **Select Region:**")
selection = st.selectbox('', RegionList)

#Filter df based on selection
Regiondf = df[ df['Regions'] == selection ]
st.write(Regiondf[['Regions','Year','Annual']])

st.subheader('Variation of the annual rain amount in %s :' % selection)

Plot = st.checkbox('Plot')
if Plot:
    fig = px.line(Regiondf, x="Year", y="Annual", text="Year")
    fig.update_traces(textposition="bottom right")
    st.write(fig)

#----------------------------------------------------------
#----------------------------------------------------------
#----------------------------------------------------------

st.header('Rain Distribution Across Cities Over The Quarters')

year_to_filter = st.slider('year', 1901, 2017, 2015)
filtered_data = df[df['Year'] == year_to_filter]

Q1 = go.Bar(x=filtered_data.Regions,
                  y=filtered_data.Q1,
                  name='Q1',
                  marker=dict(color='#1830D2'))

Q2 = go.Bar(x=filtered_data.Regions,
                y=filtered_data.Q2,
                name='Q2',
                marker=dict(color='#A25E1A'))

Q3 = go.Bar(x=filtered_data.Regions,
                y=filtered_data.Q3,
                name='Q3',
                marker=dict(color='#1DCC10'))

Q4 = go.Bar(x=filtered_data.Regions,
                  y=filtered_data.Q4,
                  name='Q4',
                  marker=dict(color='#EFEB12'))

data = [Q1, Q2, Q3, Q4]

layout = go.Layout(title="Rainfall Amount Per Quarter",
                xaxis=dict(title='Regions'),
                yaxis=dict(title='Rainfall'))

fig = go.Figure(data=data, layout=layout)

st.write(fig)
