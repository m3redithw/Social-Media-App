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
df = pd.read_csv('data/tiktok_data.csv')

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


# st.title("Dashboard")

# title
st.set_page_config(layout="wide")
# st.title('TikTok Engagement Dashboard')
# st.markdown('#### The Rise and Fall of Social Media')

# sidebar
with st.sidebar.container():
    image = Image.open('img/tiktok_logo.png')
    st.image(image,use_column_width=True)
st.sidebar.title('Pick Your Niche')
options = st.sidebar.radio('Category', options=['All', 'Food', 'Humor', 'Political', 'Fashion & Beauty', 'Fitness & Lifestyle'])

# st.header('Engagement per Niche Over Time')
# all
if options =='All':
    columns = st.columns((1,1,1,1))
    with columns[0]:
        df = train[train.views<150000000]
        fig = px.box(df, y='views', points = 'all', color_discrete_sequence = ['#3c567f'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)

    with columns[1]:
        df = train.likes
        fig = px.box(df, y='likes', points = 'all', color_discrete_sequence = ['#6975ab'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)

    with columns[2]:
        df = train[train.comments<200000]
        fig = px.box(df, y='comments', points = 'all', color_discrete_sequence = ['#9d93d5'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)

    with columns[3]:
        df = train[train.shares<1000000]
        fig = px.box(df, y='shares', points = 'all', color_discrete_sequence = ['#edd2fe'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)

# food
if options == 'Food':
    st.title('Food Content on Tiktok')
    columns = st.columns((4,1))

    with columns[0]:

        food = df[df.category=='Food']
        fig1 = px.histogram(food, x='length', title='Food Video Duration',
                           color='length', color_discrete_map={'Medium: 15-60s':'#133854', 'Short: 0-15s': '#6975ab', 'Long: 1-3mins': "#9d93d5", 'Extra-long: >3mins': '#edd2fe'},
                           labels={
                               'length':'Video Duration', 'count':'Amount of Videos'

                           })
        fig1.update_xaxes(categoryorder='array', categoryarray=['Short', 'Medium', 'Long', 'Extra-long'])
        fig1.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig1, use_container_width=True)
    with columns[1]:
        # st.markdown(" ")
        image = Image.open('img/food_size.png')
        st.image(image,use_column_width=True)
        st.markdown("#### Avg. Influencer Follower Count")
        st.markdown('***')
        image = Image.open('img/food_stats.png')
        st.image(image,use_column_width=True)


    # bottom
    st.title("Engagement Analysis")
    eng_options = ['Views', 'Likes', 'Comments', 'Shares']
    eng_selected = st.selectbox("Please select an engagement metric:", options = eng_options)

    columns = st.columns((2,3))

    # VIEWS
    if eng_selected =='Views':
        with columns[0]:
            data = train[train.category =='Food']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[800000, 18600000],
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Food'].index,
                                y = train[train.category=='Food'].views,
                                mode = 'lines',
                                name = 'Views',
                                marker=dict(
                                    color = '#A084CA'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Views Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # LIKES
    if eng_selected =='Likes':
        with columns[0]:
            data = train[train.category =='Food']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[180000, 2200000],
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Food'].index,
                                y = train[train.category=='Food'].likes,
                                mode = 'lines',
                                name = 'Likes',
                                marker=dict(
                                    color = '#D2DAFF'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Likes Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # COMMENTS
    if eng_selected =='Comments':
        with columns[0]:
            data = train[train.category =='Food']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[500, 22200],
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Food'].index,
                                y = train[train.category=='Food'].comments,
                                mode = 'lines',
                                name = 'Comments',
                                marker=dict(
                                    color = '#F1F1F1'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Comments Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # SHARES
    if eng_selected =='Shares':
        with columns[0]:

            data = train[train.category =='Food']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[0, 200000],
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Food'].index,
                                y = train[train.category=='Food'].shares,
                                mode = 'lines',
                                name = 'Shares',
                                marker=dict(
                                    color = '#BFACE0'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Shares Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

##=================================================================================##
##=================================================================================##

# humor
if options == 'Humor':
    st.title('Humor Content on Tiktok')
    columns = st.columns((4,1))
    with columns[0]:

        humor = df[df.category=='Humor']
        fig = px.histogram(humor, x='length', title='Humor Video Duration',
                           color='length', color_discrete_map={'Medium: 15-60s':'#133854', 'Short: 0-15s': '#6975ab', 'Long: 1-3mins': "#9d93d5", 'Extra-long: >3mins': '#edd2fe'},
                           labels={
                               'length':'Video Duration', 'count':'Amount of Videos'

                           })
        fig.update_xaxes(categoryorder='array', categoryarray=['Short', 'Medium', 'Long', 'Extra-long'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)
    with columns[1]:
        image = Image.open('img/humor_size.png')
        st.image(image,use_column_width=True)
        st.markdown("#### Avg. Influencer Follower Count")
        st.markdown('***')
        image = Image.open('img/humor_stats.png')
        st.image(image,use_column_width=True)

    # bottom
    st.title("Engagement Analysis")
    eng_options = ['Views', 'Likes', 'Comments', 'Shares']
    eng_selected = st.selectbox("Please select an engagement metric:", options = eng_options)

    columns = st.columns((2,3))
    # VIEWS
    if eng_selected =='Views':
        with columns[0]:
            data = train[train.category =='Humor']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[100000, 64000000], labels = {'views': "Views"},
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Humor'].index,
                                y = train[train.category=='Humor'].views,
                                mode = 'lines',
                                name = 'Views',
                                marker=dict(
                                    color = '#A084CA'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Views Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # LIKES
    if eng_selected =='Likes':
        with columns[0]:
            data = train[train.category =='Humor']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[50000, 9000000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Humor'].index,
                                y = train[train.category=='Humor'].likes,
                                mode = 'lines',
                                name = 'Likes',
                                marker=dict(
                                    color = '#D2DAFF'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Likes Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # COMMENTS
    if eng_selected =='Comments':
        with columns[0]:
            data = train[train.category =='Humor']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[3000, 55000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Humor'].index,
                                y = train[train.category=='Humor'].comments,
                                mode = 'lines',
                                name = 'Comments',
                                marker=dict(
                                    color = '#BFACE0'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Comments Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # SHARE
    if eng_selected =='Shares':
        with columns[0]:
            data = train[train.category =='Humor']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[0, 120000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Humor'].index,
                                y = train[train.category=='Humor'].shares,
                                mode = 'lines',
                                name = 'Shares',
                                marker=dict(
                                    color = '#F1F1F1'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Shares Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

##=================================================================================##
##=================================================================================##

# political
if options == 'Political':
    st.title('Political Content on Tiktok')
    columns = st.columns((4,1))
    with columns[0]:

        political = df[df.category=='Political']
        fig = px.histogram(political, x='length', title='Political Video Duration',
                           color='length', color_discrete_map={'Medium: 15-60s':'#133854', 'Short: 0-15s': '#6975ab', 'Long: 1-3mins': "#9d93d5", 'Extra-long: >3mins': '#edd2fe'},
                           labels={
                               'length':'Video Duration', 'count':'Amount of Videos'

                           })
        fig.update_xaxes(categoryorder='array', categoryarray=['Short', 'Medium', 'Long', 'Extra-long'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)

    with columns[1]:
        image = Image.open('img/political_size.png')
        st.image(image,use_column_width=True)
        st.markdown("#### Avg. Influencer Follower Count")
        st.markdown('***')
        image = Image.open('img/political_stats.png')
        st.image(image,use_column_width=True)


    # bottom
    st.title("Engagement Analysis")
    eng_options = ['Views', 'Likes', 'Comments', 'Shares']
    eng_selected = st.selectbox("Please select an engagement metric:", options = eng_options)
    columns = st.columns((2,3))

    # VIEWS
    if eng_selected =='Views':
        with columns[0]:
            data = train[train.category =='Political']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[100000, 9000000],labels = {'views': "Views"},
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Political'].index,
                                y = train[train.category=='Political'].views,
                                mode = 'lines',
                                name = 'Views',
                                marker=dict(
                                    color = '#A084CA'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Views Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # LIKES
    if eng_selected =='Likes':
        with columns[0]:
            data = train[train.category =='Political']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[10000, 1000000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Political'].index,
                                y = train[train.category=='Political'].likes,
                                mode = 'lines',
                                name = 'Likes',
                                marker=dict(
                                    color = '#D2DAFF'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Likes Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

    # COMMENTS
    if eng_selected =='Comments':
        with columns[0]:
            data = train[train.category =='Political']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[1000, 35000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Political'].index,
                                y = train[train.category=='Political'].comments,
                                mode = 'lines',
                                name = 'Comments',
                                marker=dict(
                                    color = '#BFACE0'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Comments Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # SHARES
    if eng_selected =='Shares':
        with columns[0]:
            data = train[train.category =='Political']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[500, 80000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Political'].index,
                                y = train[train.category=='Political'].shares,
                                mode = 'lines',
                                name = 'Shares',
                                marker=dict(
                                    color = '#F1F1F1'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Shares Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

##=================================================================================##
##=================================================================================##

# fashion
if options == 'Fashion & Beauty':
    st.title('Fashion & Beauty Content on Tiktok')
    columns = st.columns((4,1))
    with columns[0]:

        fashion = df[df.category=='Fashion']
        fig = px.histogram(fashion, x='length', title='Fashion & Beauty Video Duration',
                           color='length', color_discrete_map={'Medium: 15-60s':'#133854', 'Short: 0-15s': '#6975ab', 'Long: 1-3mins': "#9d93d5", 'Extra-long: >3mins': '#edd2fe'},
                           labels={
                               'length':'Video Duration', 'count':'Amount of Videos'

                           })
        fig.update_xaxes(categoryorder='array', categoryarray=['Short', 'Medium', 'Long', 'Extra-long'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)
    with columns[1]:
        image = Image.open('img/fashion_size.png')
        st.image(image,use_column_width=True)
        st.markdown("#### Avg. Influencer Follower Count")
        st.markdown('***')
        image = Image.open('img/fashion_stats.png')
        st.image(image,use_column_width=True)
    # bottom
    st.title("Engagement Analysis")
    eng_options = ['Views', 'Likes', 'Comments', 'Shares']
    eng_selected = st.selectbox("Please select an engagement metric:", options = eng_options)
    columns = st.columns((2,3))

    # VIEWS
    if eng_selected =='Views':
        with columns[0]:
            data = train[train.category =='Fashion']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[100000, 25000000],labels = {'views': "Views"},
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Fashion'].index,
                                y = train[train.category=='Fashion'].views,
                                mode = 'lines',
                                name = 'Views',
                                marker=dict(
                                    color = '#A084CA'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Views Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

    # LIKES
    if eng_selected =='Likes':
        with columns[0]:
            data = train[train.category =='Fashion']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[10200, 4000000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Fashion'].index,
                                y = train[train.category=='Fashion'].likes,
                                mode = 'lines',
                                name = 'Likes',
                                marker=dict(
                                    color = '#D2DAFF'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Likes Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

    # COMMENTS
    if eng_selected =='Comments':
        with columns[0]:
            data = train[train.category =='Fashion']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[300, 160000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Fashion'].index,
                                y = train[train.category=='Fashion'].comments,
                                mode = 'lines',
                                name = 'Comments',
                                marker=dict(
                                    color = '#BFACE0'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Comments Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

    # SHARES
    if eng_selected =='Shares':
        with columns[0]:
            data = train[train.category =='Fashion']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[0, 100000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Fashion'].index,
                                y = train[train.category=='Fashion'].shares,
                                mode = 'lines',
                                name = 'Shares',
                                marker=dict(
                                    color = '#F1F1F1'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Shares Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

##=================================================================================##
##=================================================================================##

# fitness
if options == 'Fitness & Lifestyle':
    st.title('Fitness & Lifestyle Content on Tiktok')
    columns = st.columns((4,1))
    with columns[0]:
        fitness = df[df.category=='Fitness & Lifestyle']
        fig = px.histogram(fitness, x='length', title='Fitness & Lifestyle Video Duration',
                           color='length', color_discrete_sequence=['#133854', '#9d93d5','#6975ab', '#edd2fe'],
                           labels={
                               'length':'Video Duration', 'count':'Amount of Videos'

                           })
        fig.update_xaxes(categoryorder='array', categoryarray=['Short', 'Medium', 'Long', 'Extra-long'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)
    with columns[1]:
        image = Image.open('img/fitness_size.png')
        st.image(image,use_column_width=True)
        st.markdown("#### Avg. Influencer Follower Count")
        st.markdown('***')
        image = Image.open('img/fitness_stats.png')
        st.image(image,width = 350)
    # bottom
    st.title("Engagement Analysis")
    eng_options = ['Views', 'Likes', 'Comments', 'Shares']
    eng_selected = st.selectbox("Please select an engagement metric:", options = eng_options)
    columns = st.columns((2,3))

    # VIEWS
    if eng_selected =='Views':
        with columns[0]:

            data = train[train.category =='Fitness & Lifestyle']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[0, 25000000],labels = {'views': "Views"},
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Fitness & Lifestyle'].index,
                                y = train[train.category=='Fitness & Lifestyle'].views,
                                mode = 'lines',
                                name = 'Views',
                                marker=dict(
                                    color = '#A084CA'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Views Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

    # LIKES
    if eng_selected =='Likes':
        with columns[0]:
            data = train[train.category =='Fitness & Lifestyle']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[0, 4000000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Fitness & Lifestyle'].index,
                                y = train[train.category=='Fitness & Lifestyle'].likes,
                                mode = 'lines',
                                name = 'Likes',
                                marker=dict(
                                    color = '#D2DAFF'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Likes Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)

    # COMMENTS
    if eng_selected =='Comments':
        with columns[0]:
            data = train[train.category =='Fitness & Lifestyle']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[0, 50000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Fitness & Lifestyle'].index,
                                y = train[train.category=='Fitness & Lifestyle'].comments,
                                mode = 'lines',
                                name = 'Comments',
                                marker=dict(
                                    color = '#BFACE0'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Comments Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)


    # SHARES
    if eng_selected =='Shares':
        with columns[0]:
            data = train[train.category =='Fitness & Lifestyle']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[0, 120000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = train[train.category=='Fitness & Lifestyle'].index,
                                y = train[train.category=='Fitness & Lifestyle'].shares,
                                mode = 'lines',
                                name = 'Shares',
                                marker=dict(
                                    color = '#F1F1F1'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Shares Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)
