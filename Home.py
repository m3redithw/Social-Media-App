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


# read in data
path = '/Users/williambaldridge/codeup-data-science/streamlit/'

df = pd.read_csv(path+'data/tiktok_data.csv')

# clean df
df = prepare.prep_tiktok(df)

# set date as index
df.set_index('date', inplace=True)
df = df.sort_index()

# trim off dates
df = df[df.index >= '2018-12-01']
df = df[df.index <= '2022-09-10']

# train dataset
train_size = int(round(df.shape[0] * 0.5)+1)
train = df[:train_size]
train = train.sort_index()


st.set_page_config(page_title='Home',
                   page_icon='😀',
                   layout="wide")
image = Image.open('img/title.png')
st.image(image,use_column_width=True)
# st.sidebar.success("Select a page above.")

# st.title('TikTok Engagement Dashboard')
# st.markdown('#### The Rise and Fall of Social Media')

