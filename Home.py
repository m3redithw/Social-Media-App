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
        image = Image.open('img/foryou.png')
        st.image(image,use_column_width=True)


    with tab2:
        ## DESCRIPTION
        title = '<p style=" color:#dfaeff; font-size: 30px;"><b>Project Description</b></p>'
        st.markdown(title, unsafe_allow_html=True)

        st.write('TikTok, a video sharing and relatively new social media platform (funded in 2016), '
                'has gained tremendous amount of popularity over the past few years. '
                 'Understanding their "success metric" and knowing how to attract engagement is extremely important '
                 'for business and individuals who want to develop their presence on there.')
        st.write('This APP is an additional component to the project for both technical and non-technical skate-holders to grasp the key findings. '
                 'If you are interested in the "behind-the-scene", please feel free to visit our [GitHub](https://github.com/Social-Media-Capstone/Social-Media-Engagement-Forecasting). ')


        ## BUSINESS GOALS
        title = '<p style=" color:#dfaeff; font-size: 30px;"><b>Business Goal</b></p>'
        st.markdown(title, unsafe_allow_html=True)

        st.write('We used time series models to forecast engagement over time, along with natural language processing regression models to predict '
                 'the key words that are likely to generate viral content. E-commerce, retail businesses, influencers, etc. can stratigically utilize our'
                 'predictive model to push out content that would gain the most branded-effect possible with worlwide audience and generate revenue.')


        ##DATA OVERVIEW
        title = '<p style=" color:#dfaeff; font-size: 30px;"><b>Data Overview</b></p>'
        st.markdown(title, unsafe_allow_html=True)

        st.write('We acquired data of 3 major social media platforms: TikTok, YouTube, and Instagram. '
                 'Data is acquired through 5 web-scraping tools and 3 third-party APIs. '
                 "In total, we gathered 1.6 million-records of data including:")
        st.write('\n')
        st.write("▪️ videos/posts metadata")
        st.write('\n')
        st.write("▪️ creators' stats")
        st.write('\n')
        st.write("▪️ trending-content engagement data.")

        ## DEPENDENCIES
        title = '<p style=" color:#dfaeff; font-size: 30px;"><b>Project Dependencies</b></p>'
        st.markdown(title, unsafe_allow_html=True)
        st.markdown('[![python-shield](https://img.shields.io/badge/Python-F8EEFF?&logo=python&logoColor=white)](https://www.python.org/)')
        st.markdown('[![python-shield](https://img.shields.io/badge/Python-F8EEFF?&logo=python&logoColor=white)](https://www.python.org/)')
        st.markdown('[![numpy-shield](https://img.shields.io/badge/Numpy-EED6FF?&logo=NumPy)](https://numpy.org/)')
        st.markdown('[![pandas-shield](https://img.shields.io/badge/Pandas-EBCEFF?&logo=pandas)](https://pandas.pydata.org/)')
        st.markdown('[![matplotlib-shield](https://img.shields.io/badge/Matplotlib-E8C6FF.svg?)](https://matplotlib.org)')
        st.markdown('[![seaborn-shield](https://img.shields.io/badge/Seaborn-E5BEFF?&logo=python-seaborn&logoColor=white)](https://seaborn.pydata.org/)')
        st.markdown('[![plotly-shield](https://img.shields.io/badge/Plotly-E2B6FF?&logo=Plotly&logoColor=white)]([https://seaborn.pydata.org/](https://plotly.com/python/))')
        st.markdown('[![scipy-shield](https://img.shields.io/badge/SciPy-dfaeff?&logo=scipy&logoColor=white)](https://scipy.org/)')
        st.markdown('[![sklearn-shield](https://img.shields.io/badge/sklearn-C89CE5?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/stable/)')
        st.markdown('[![Tensorflow-shield](https://img.shields.io/badge/Tensorflow-B28BCC?logo=tensorflow&logoColor=white)](https://scikit-learn.org/stable/)')
        st.markdown('[![prophet-shield](https://img.shields.io/badge/FacebookProphet-9C79B2?logoColor=white)](https://scikit-learn.org/stable/)')
        st.markdown('[![nltk-shield](https://img.shields.io/badge/NLTK-856899?&logo=&logoColor=white)](https://textblob.readthedocs.io/en/dev/)')
        st.markdown('[![xgboost-shield](https://img.shields.io/badge/XGBoost-6F567F?&logo=XGBoost&logoColor=white)](https://xgboost.readthedocs.io/en/stable/)')


        ## KEY FINDINGS
        title = '<p style=" color:#dfaeff; font-size: 30px;"><b>Key Findings</b></p>'
        st.markdown(title, unsafe_allow_html=True)
        st.write('▪️ Over **93%** of trending content on TikTok are short(0-15s) & medium(15-60s) videos.')
        st.write('\n')
        st.write('▪️ Video duration and engagement rate is dependent on the cateogory. For example: humor content have the highest performance with extra-long (>3mins) videos, whereas political content perform the best with short (0-15s) videos.')
        st.write('\n')
        st.write('▪️ Trending content of all categories on TikTok have **11M** views, **1.4M** likes, **10.7K** comments, and **34.5K** shares on average.')
        st.write('\n')
        st.write('▪️ Total engagement of 2-year global trending content of each platform: TikTok is **6x** more than YouTube, and more than **1000x** more than Instagram.')
        st.write('\n')
        st.write('▪️ TikTok total engagement has increased **980%** from 2019 to Sep 2022.')
        st.write('\n')
        st.write('▪️ TikTok users respond to major **social/political events** significantly. Engagement peak/rise present prior, during, and after time period of the events.')
        st.write('\n')
        st.write("▪️ Trending content creators' follower size has decreased since Jan 2021. TikTok's algorithm has been incentivizing small creators to push out content.")
        st.write('\n')
        st.write('▪️ Facebook Prophet model forecast engagement with 57% improvement compared to baseline. ')
        st.write('\n')
        st.write('▪️ Content-description text frequency **DOES NOT** correlate with engagement. There are specific words that drive engagement for each niche. Our natural language processing general linear model predicts word choice 42% more accurate than baseline.')
        st.write('\n')
        st.write('▪️ Total engagement on TikTok is predicted to increase **27%** within the next year (Oct 2022 - Oct 2023). ')

        ## KEY FINDINGS
        title = '<p style=" color:#dfaeff; font-size: 30px;"><b>Future Development</b></p>'
        st.markdown(title, unsafe_allow_html=True)
        st.write('Despite the overall effectiveness of our best-performing model, there is always room for improvement and optimization. \n We are currently working on future devlopenet including:')
        st.write('\n')
        st.write('▪️ Examining the differences between influencers and common users.')
        st.write('\n')
        st.write('▪️ Including more niches/categories into our scope. For example: pets, sports, dance.')
        st.write('\n')
        st.write('▪️ Doing bi-gram & tri-gram analysis on content description as long as the content of comments on videos.')
        st.write('\n')
        st.write("▪️ Getting users' demographic data and analyzing the relatinship of location, user's age, etc. with engagement.")
