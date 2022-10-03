import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import plotly.offline as pyo
import plotly.graph_objs as go
import scipy
import datetime
from PIL import Image
# functions
def prep_tiktok(df):
    '''
    This funciton takes in messy tiktok data and return the cleaned version
    '''
    #df.drop(columns = 'Unnamed: 0', inplace = True)
    df.rename(columns = {'commentCount':'comments', 'diggCount':'likes',
                         'playCount':'views', 'shareCount':'shares', 'time':'epoch',
                         'followerCount': 'total_followers',
                         'heartCount':'total_likes',
                         'videoCount': 'total_videos'}, inplace=True)
    df['date'] = (pd.to_datetime(df['epoch'], unit='s')
                  .dt.tz_localize('utc')
                  .dt.tz_convert('US/Central'))
    df['date'] = df['date'].astype(str)
    df['date'] = df['date'].str.slice(0,10)
    df.date = pd.to_datetime(df.date)
    df.drop(columns = 'epoch', inplace = True)
    # locate duration = 0 columns
    indexname = df[df.duration ==0].index
    # drop rows with duration = 0
    df.drop(indexname, inplace=True)
    # convert date
    df.date = pd.to_datetime(df.date)
    # df.set_index('date', inplace=True)
    # df.sort_index()
    df['category'].replace({
        'fashion': 'Fashion',
        'fitness & lifestyle': 'Fitness & Lifestyle',
        'food': 'Food',
        'humor': 'Humor',
        'political': 'Political'}, inplace=True)
    # create conditions
    conditions = [(df['duration']<=15),
                  (df['duration']>15)&(df['duration']<=60),
                  (df['duration']>60)&(df['duration']<=180),
                  (df['duration']>180)]
    values = ['Short: 0-15s', 'Medium: 15-60s', 'Long: 1-3mins', 'Extra-long: >3mins']
    # create length column using conditions
    df['length'] = np.select(conditions, values)

    return df



# read in data
df = pd.read_csv('data/tiktok_data.csv')
tiktok = pd.read_csv('data/tiktok_data.csv')
# clean df
df = prep_tiktok(df)
tiktok = prep_tiktok(tiktok)
tiktok = tiktok[tiktok.date >= '2018-12-01']
tiktok = tiktok[tiktok.date <= '2022-09-10']

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
    st.markdown('## TikTok Video Content Duration')
    columns = st.columns((3, 1.5))

    with columns[0]:
        # BARCHART

        fig = px.histogram(df, x='length', title='Content Length Distribution', template = "plotly_dark",
                           color='length', color_discrete_map={'Medium: 15-60s':'#133854', 'Short: 0-15s': '#6975ab', 'Long: 1-3mins': "#9d93d5", 'Extra-long: >3mins': '#edd2fe'},
                           labels={
                               'length':'Video Duration', 'count':'Amount of Videos'

                           })
        fig.update_xaxes(categoryorder='array', categoryarray=['Medium: 15-60s', 'Short: 0-15s', 'Long: 1-3mins', 'Extra-long: >3mins'])
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size=16)
        st.plotly_chart(fig, use_container_width=True)

    with columns[1]:
        # VIDEO LENGTH DISTPLOT
        x = df[df.duration<200]['duration']
        hist_data = [x]
        group_labels = ['Video Duration'] # name of the dataset

        fig = ff.create_distplot(hist_data, group_labels, colors = ['#f3e2fe'])
        fig.update_layout(title_text='Video Duration (by second) Distribution', paper_bgcolor="#202020", plot_bgcolor='#202020', font_size = 16, height=500)
        st.plotly_chart(fig, use_container_width=True)

    # ENGAGEMENT STATS
    st.markdown('## Engagement Stats')
    st.text("NOTE: stats directly below this line represents the average of each engagement metric.")
    columns = st.columns((1,1,1,1))
    with columns[0]:
        image = Image.open('img/views.png')
        st.image(image,use_column_width=True)

        # boxplot
        df1 = df[df.views<165000000]
        fig = px.box(df1, y='views', points = 'all', color_discrete_sequence = ['#3c567f'], labels ={'views':'Views'})
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16, height = 500)
        st.plotly_chart(fig, use_container_width=True)

    with columns[1]:
        image = Image.open('img/likes.png')
        st.image(image,use_column_width=True)

        # boxplot
        df1 = df.likes
        fig = px.box(df1, y='likes', points = 'all', color_discrete_sequence = ['#6975ab'],  labels ={'likes':'Likes'})
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16, height = 500)
        st.plotly_chart(fig, use_container_width=True)

    with columns[2]:
        image = Image.open('img/comments.png')
        st.image(image,use_column_width=True)

        # boxplot
        df1 = df[df.comments<218000]
        fig = px.box(df1, y='comments', points = 'all', color_discrete_sequence = ['#edd2fe'],  labels ={'comments':'Comments'})
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16, height = 500)
        st.plotly_chart(fig, use_container_width=True)

    with columns[3]:
        image = Image.open('img/shares.png')
        st.image(image,use_column_width=True)

        # boxplot
        df1 = df[df.shares<1200000]
        fig = px.box(df1, y='shares', points = 'all', color_discrete_sequence = ['#9d93d5'],  labels ={'shares':'Shares'})
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16, height = 500)
        st.plotly_chart(fig, use_container_width=True)
##=================================================================================##
    # 3rd ROW
    st.markdown('## Platform Engagement Comparison')
    stats = pd.DataFrame({'Trending Content Avg. Engagement': [11237882,1790364,10414], 'Platform': ['TikTok', 'YouTube', 'Instagram']})
    fig = px.bar(stats, x='Platform', y='Trending Content Avg. Engagement', color = 'Platform', color_discrete_map={'YouTube':'#dfaeff', 'TikTok': '#3C567F',
                                                                                                'Instagram': "#f3e2fe"})
    fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16, height = 500)
    st.plotly_chart(fig, use_container_width=True)

##=================================================================================##

    # 4th ROW
    columns = st.columns((1,1))
    with columns[0]:
        st.markdown("## Creator's Follower Count vs. Total Engagement")
        fig = px.scatter(tiktok, x='total_followers', y='likes', color = 'category',
                   color_discrete_map={'Fashion':'#6975AB', 'Food': '#3C567F',
                                       'Humor': "#133854", 'Political': '#D7B1FA', 'Fitness & Lifestyle': '#9D93D5'},
                   labels ={'likes':'Total Engagement', 'total_followers':"Creator's Follower Count"})
        fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
        st.plotly_chart(fig, use_container_width=True)
        st.text("Fashion content's engagement has the strongest correlation with creator's follower count.")
    with columns[1]:
        st.markdown("## Engagment vs. Video Length per Category")
        options = ['Views', 'Likes', 'Comments', 'Shares']
        selected = st.selectbox("Please select an engagement metric:", options = options)
        if selected == 'Views':
            view_data = pd.DataFrame(tiktok.groupby(['category', 'length'])['views'].mean()).reset_index()
            fig = px.bar(view_data, x='length', y='views', color = 'category',
                         color_discrete_map={'Fashion':'#6975AB', 'Food': '#3C567F',
                                             'Humor': "#133854", 'Political': '#D7B1FA', 'Fitness & Lifestyle': '#9D93D5'},
                         barmode = 'group', labels ={'length':'Video Length', 'views':'Views'})
            fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
            st.plotly_chart(fig, use_container_width=True)

        if selected == 'Likes':
            like_data = pd.DataFrame(tiktok.groupby(['category', 'length'])['likes'].mean()).reset_index()
            fig = px.bar(like_data, x='length', y='likes', color = 'category',
                         color_discrete_map={'Fashion':'#6975AB', 'Food': '#3C567F',
                                             'Humor': "#133854", 'Political': '#D7B1FA', 'Fitness & Lifestyle': '#9D93D5'},
                         barmode = 'group', labels ={'length':'Video Length', 'likes':'Likes'})
            fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
            st.plotly_chart(fig, use_container_width=True)

        if selected == 'Comments':
            comment_data = pd.DataFrame(tiktok.groupby(['category', 'length'])['comments'].mean()).reset_index()
            fig = px.bar(comment_data, x='length', y='comments', color = 'category',
                         color_discrete_map={'Fashion':'#6975AB', 'Food': '#3C567F',
                                             'Humor': "#133854", 'Political': '#D7B1FA', 'Fitness & Lifestyle': '#9D93D5'},
                         barmode = 'group', labels ={'length':'Video Length', 'comments':'Comments'})
            fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
            st.plotly_chart(fig, use_container_width=True)

        if selected == 'Shares':
            share_data = pd.DataFrame(tiktok.groupby(['category', 'length'])['shares'].mean()).reset_index()
            fig = px.bar(share_data, x='length', y='shares', color = 'category',
                         color_discrete_map={'Fashion':'#6975AB', 'Food': '#3C567F',
                                             'Humor': "#133854", 'Political': '#D7B1FA', 'Fitness & Lifestyle': '#9D93D5'},
                         barmode = 'group', labels ={'length':'Video Length', 'shares':'Shares'})
            fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16)
            st.plotly_chart(fig, use_container_width=True)

##=================================================================================##
##=================================================================================##
    # BOTTOM
    st.markdown('## Engagement Over Time')
    resample = df.resample('w')[['comments', 'likes', 'views', 'shares']].sum()
    fig = px.line(resample, x=resample.index, y='views', color_discrete_sequence=['#E80F88'])
    # Hong Kong
    fig.add_vrect(x0='2019-03-15', x1="2019-06-22", fillcolor="#D2DAFF", opacity = 0.25)
    fig.add_annotation(x='2019-05-09', y=500000000, text = 'Hong Kong Protest', yshift = 5)

    # COVID
    fig.add_vrect(x0='2020-02-01', x1="2020-04-28", fillcolor="#D2DAFF", opacity = 0.25)
    fig.add_annotation(x='2020-03-20', y=3500000000, text = 'COVID-19 Outbreak', yshift = 5)

    fig.add_vrect(x0="2020-05-24", x1='2020-08-13', annotation_text='George Floyd Protests', annotation_position='bottom left', fillcolor = '#D2DAFF', opacity=0.25)
    # fig.add_vrect(x0="2021-07-29", x1='2021-07-29', annotation_text='Biden Vaccine Mandate', annotation_position='top left', fillcolor = '#D2DAFF', opacity=0.8)

    # Election Day
    fig.add_vline(x="2020-12-13", line_width=3, line_dash="dash", line_color="#D2DAFF")
    fig.add_annotation(x='2020-12-13', y=1720000000, text = 'Election Day', yshift = 10)

    # Vaccine Mandate
    fig.add_vline(x='2021-07-29', line_width=3, line_dash="dash", line_color="#D2DAFF" )
    fig.add_annotation(x='2021-07-29', y=2000000000, text = 'Biden Vaccine Mandate', yshift = 10)

    # Chris Rock
    fig.add_vline(x="2022-04-10", line_width=3, line_dash="dash", line_color="#D2DAFF")
    fig.add_annotation(x='2022-04-10', y = 3200000000, text = 'Chris Rock & Will Smith', yshift=10)

    fig.update_layout(paper_bgcolor="#202020", plot_bgcolor='#202020', font_color='#f3e2fe', font_size = 16, height = 500)
    fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(showgrid=False)


    st.plotly_chart(fig, use_container_width=True, )


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
            data = df[df.category =='Food']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[800000, 18600000],
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Food'].index,
                                y = df[df.category=='Food'].views,
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
            data = df[df.category =='Food']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[180000, 2200000],
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Food'].index,
                                y = df[df.category=='Food'].likes,
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
            data = df[df.category =='Food']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[500, 22200],
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Food'].index,
                                y = df[df.category=='Food'].comments,
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

            data = df[df.category =='Food']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[0, 200000],
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Food'].index,
                                y = df[df.category=='Food'].shares,
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
        st.markdown("#### Avg. Creator Follower Count")
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
            data = df[df.category =='Humor']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[100000, 64000000], labels = {'views': "Views"},
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Humor'].index,
                                y = df[df.category=='Humor'].views,
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
            data = df[df.category =='Humor']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[50000, 9000000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Humor'].index,
                                y = df[df.category=='Humor'].likes,
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
            data = df[df.category =='Humor']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[3000, 55000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Humor'].index,
                                y = df[df.category=='Humor'].comments,
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
            data = df[df.category =='Humor']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[0, 120000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)

        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Humor'].index,
                                y = df[df.category=='Humor'].shares,
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
            data = df[df.category =='Political']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[100000, 9000000],labels = {'views': "Views"},
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Political'].index,
                                y = df[df.category=='Political'].views,
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
            data = df[df.category =='Political']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[10000, 2000000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Political'].index,
                                y = df[df.category=='Political'].likes,
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
            data = df[df.category =='Political']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[1000, 35000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Political'].index,
                                y = df[df.category=='Political'].comments,
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
            data = df[df.category =='Political']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[500, 80000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Political'].index,
                                y = df[df.category=='Political'].shares,
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
            data = df[df.category =='Fashion']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[100000, 30000000],labels = {'views': "Views"},
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Fashion'].index,
                                y = df[df.category=='Fashion'].views,
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
            data = df[df.category =='Fashion']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[10200, 4000000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Fashion'].index,
                                y = df[df.category=='Fashion'].likes,
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
            data = df[df.category =='Fashion']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[300, 160000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Fashion'].index,
                                y = df[df.category=='Fashion'].comments,
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
            data = df[df.category =='Fashion']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[0, 100000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Fashion'].index,
                                y = df[df.category=='Fashion'].shares,
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

            data = df[df.category =='Fitness & Lifestyle']
            fig = px.histogram(
                data, x="views",
                marginal = 'rug',range_x=[0, 25000000],labels = {'views': "Views"},
                title='Avg. View Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Fitness & Lifestyle'].index,
                                y = df[df.category=='Fitness & Lifestyle'].views,
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
            data = df[df.category =='Fitness & Lifestyle']
            fig = px.histogram(
                data, x="likes",
                marginal = 'rug',range_x=[0, 4000000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Fitness & Lifestyle'].index,
                                y = df[df.category=='Fitness & Lifestyle'].likes,
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
            data = df[df.category =='Fitness & Lifestyle']
            fig = px.histogram(
                data, x="comments",
                marginal = 'rug',range_x=[0, 50000],labels = {'views': "Views"},
                title='Avg. Comment Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Fitness & Lifestyle'].index,
                                y = df[df.category=='Fitness & Lifestyle'].comments,
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
            data = df[df.category =='Fitness & Lifestyle']
            fig = px.histogram(
                data, x="shares",
                marginal = 'rug',range_x=[0, 120000],labels = {'views': "Views"},
                title='Avg. Like Count per Video', color_discrete_sequence=['#dfaeff'])
            fig.update_layout({'plot_bgcolor': '#202020', 'paper_bgcolor': '#202020'})
            st.plotly_chart(fig, use_container_width=True)
        with columns[1]:
            trace1 = go.Scatter(x = df[df.category=='Fitness & Lifestyle'].index,
                                y = df[df.category=='Fitness & Lifestyle'].shares,
                                mode = 'lines',
                                name = 'Shares',
                                marker=dict(
                                    color = '#F1F1F1'
                                ))
            data = [trace1]
            layout = go.Layout(title = 'Shares Over Time', plot_bgcolor='#202020', paper_bgcolor='#202020')
            fig = go.Figure(data = data, layout = layout)
            st.plotly_chart(fig, use_container_width=True)
