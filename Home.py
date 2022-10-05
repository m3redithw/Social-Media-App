import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.offline as pyo
import plotly.graph_objs as go
import datetime
from PIL import Image
# functions
import prepare

# page config
st.set_page_config(page_title='Home',
                   page_icon='😀',
                   layout="wide")

# tabs
columns = st.columns((0.5,1,0.5))
with columns[1]:

    tab1, tab2 = st.tabs(['Following', 'For You'])

    with tab1:
        st.text('work in progress')

    with tab2:
        image = Image.open('img/foryou.png')
        st.image(image,use_column_width=True)

# with columns[2]:
#     image = Image.open('img/search.png')
#     st.image(image,width=100)