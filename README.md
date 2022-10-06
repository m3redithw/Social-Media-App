# Social Media Engagement Forecasting Web App
by **Meredith Wang**

September 2022 - Present

<img width="424" alt="foryou" src="https://user-images.githubusercontent.com/105242871/194430932-426aed6f-aa42-4f58-ac9a-09f17669067a.png">


# Description
TikTok, a video sharing and relatively new social media platform (funded in 2016), has gained tremendous amount of popularity over the past few years. Understanding their "success metric" and knowing how to attract engagement is extremely important for business and individuals who want to develop their presence on there.

This APP is an additional component to the project for both technical and non-technical skate-holders to grasp the key findings. If you are interested in the "behind-the-scene", please feel free to visit our [GitHub](https://github.com/Social-Media-Capstone/Social-Media-Engagement-Forecasting).

# Business Goal
We used time series models to forecast engagement over time, along with natural language processing regression models to predict the key words that are likely to generate viral content. E-commerce, retail businesses, influencers, etc. can stratigically utilize ourpredictive model to push out content that would gain the most branded-effect possible with worlwide audience and generate revenue.

# Data Overview
We acquired data of 3 major social media platforms: **TikTok**, **YouTube**, and **Instagram**. Data is acquired through 5 web-scraping tools and 3 third-party APIs. In total, we gathered 1.6 million-records of data including:

▪️ videos/posts metadata

▪️ creators' stats

▪️ trending-content engagement data.

# Dependencies
* [![python-shield](https://img.shields.io/badge/Python-dfaeff?&logo=python&logoColor=white)
    ](https://www.python.org/)
* [![numpy-shield](https://img.shields.io/badge/Numpy-dfaeff?&logo=NumPy)
    ](https://numpy.org/)
* [![pandas-shield](https://img.shields.io/badge/Pandas-dfaeff?&logo=pandas)
    ](https://pandas.pydata.org/)
* [![plotly-shield](https://img.shields.io/badge/Plotly-dfaeff?&logo=Plotly&logoColor=white)
    ]([https://seaborn.pydata.org/](https://plotly.com/python/))


# Key Findings
▪️ Over 93% of trending content on TikTok are short(0-15s) & medium(15-60s) videos.

▪️ Video duration and egagement rate is dependent on the cateogory. For example: humor content have the highest performance with extra-long (>3mins) videos, whereas political content perform the best with short (0-15s) videos.

▪️ Trending content of all categories on TikTok have 11M views, 1.4M likes, 10.7K comments, and 34.5K shares on average.

▪️ Total engagement of 2-year global trending content of each platform: TikTok is 6x more than YouTube, and more than 1000x more than Instagram.

▪️ TikTok total engagement has increased 980% from 2019 to Sep 2022.

▪️ TikTok users respond to major social/political events significantly. Engagement peak/rise present prior, during, and after time period of the events.

▪️ Trending content creators' follower size has decreased since Jan 2021. TikTok's algorithm has been incentivizing small creators to push out content.

▪️ Facebook Prophet model forecast engagement with 57% improvement compared to baseline.

▪️ Content-description text frequency DOES NOT correlate with engagement. There are specific words that drive engagement for each niche. Our natural language processing general linear model predicts word choice 42% more accurate than baseline.

▪️ Total engagement on TikTok is predicted to increase 27% within the next year (Oct 2022 - Oct 2023).

# Future Development
Despite the overall effectiveness of our best-performing model, there is always room for improvement and optimization. We are currently working on future devlopenet including:

▪️ Examining the differences between influencers and common users.

▪️ Including more niches/categories into our scope. For example: pets, sports, dance.

▪️ Doing bi-gram & tri-gram analysis on content description as long as the content of comments on videos.
    
