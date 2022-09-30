import streamlit as st
from PIL import Image
path = '/Users/williambaldridge/codeup-data-science/streamlit/'
st.title("Data Science Team")

with st.container():
    columns = st.columns((1,5))
    with columns[0]:

        image = Image.open(path+'img/Brad.jpg')
        st.image(image,use_column_width=True)
    with columns[1]:
        st.title('Brad Gauvin')
        st.write('Gmail: bradly.gauvin@gmail.com')
        st.write('Linkedin: [@bradleygauvin](https://www.linkedin.com/in/bradleygauvin/)')
        st.write('GitHub: [@bradgauvin](https://github.com/bradgauvin)')
        st.write('Contribution: Acquisition, Final Report, Dashboard Design, Project Advisor')

st.markdown('***')

with st.container():
    columns = st.columns((1,5))
    with columns[0]:

        image = Image.open(path+'img/Jess.png')
        st.image(image,use_column_width=True)
    with columns[1]:
        st.title('Jessica Gardin')
        st.write('Gmail: jess.gardin88@gmail.com')
        st.write('Linkedin: [@jessgardin](https://www.linkedin.com/in/jessgardin/)')
        st.write('GitHub: [@Jgardin875](https://github.com/Jgardin875)')
        st.write('Contribution: Acquisition, Preparation, Exploration, NLP Analysis, Modeling, Final Report, Slide Deck, Project Advisor')

st.markdown('***')

with st.container():
    columns = st.columns((1,5))
    with columns[0]:

        image = Image.open(path+'img/Saroj.jpg')
        st.image(image,use_column_width=True)
    with columns[1]:
        st.title('Saroj Duwal')
        st.write('Gmail: saroj.duwal@gmail.com')
        st.write('Linkedin: [@sarojduwal](https://www.linkedin.com/in/sarojduwal/)')
        st.write('GitHub: [@Saroj6632](https://github.com/Saroj6632)')
        st.write('Contribution: Acquisition, Exploration, README.md')

st.markdown('***')

with st.container():
    columns = st.columns((1,5))
    with columns[0]:

        image = Image.open(path+'img/Meredith.jpg')
        st.image(image,use_column_width=True)
    with columns[1]:
        st.title('Meredith Wang')
        st.write('Gmail: wang.meredith09@gmail.com')
        st.write('Linkedin: [@m3redithw](https://www.linkedin.com/in/m3redithw/)')
        st.write('GitHub: [@m3redithw](https://github.com/m3redithw)')
        st.write('Contribution: Acquisition, Preparation, Exploration, Modeling, Final Report, Web Development, Dashboard Design, Slide Deck')