import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from bs4 import BeautifulSoup
import requests
import random
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode

def GET_UA():
    uastrings = ["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",\
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",\
                "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0",\
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36"\
                ]

    return random.choice(uastrings)

url = "https://www.metacritic.com/browse/movies/score/metascore/year/filtered?year_selected=2022"
user_agent = {'User-agent': GET_UA()}
response = requests.get(url, headers = user_agent)

soup = BeautifulSoup(response.text, 'html.parser')

review_dict = {'name':[], 'date':[], 'critic_score':[], 'user_score':[]}

for title in soup.find_all('a', class_='title'): 
    movie_title = title.text
    # movie_title
    review_dict['name'].append(movie_title)
for date in soup.find_all('div', class_='clamp-details'):
    date_span = date.span
    for span in date_span: 
        release_date = span.text
        # release_date
        review_dict['date'].append(release_date)
for review in soup.find_all('div', class_='clamp-metascore'):
    critic_div = review.find('div', class_='metascore_w large movie positive')
    critic_score = critic_div.text
    # critic_score
    review_dict['critic_score'].append(critic_score)
for review in soup.find_all('div', class_='clamp-userscore'):
    if review.find('div', class_='metascore_w user large movie positive'):
        user_pos_div = review.find('div', class_='metascore_w user large movie positive')
        user_pos = user_pos_div.text
        # user_pos
        review_dict['user_score'].append(user_pos)
    if review.find('div', class_='metascore_w user large movie mixed'):
        user_mix_div = review.find('div', class_='metascore_w user large movie mixed')
        user_mix = user_mix_div.text
        # user_mix
        review_dict['user_score'].append(user_mix)
    if review.find('div', class_='metascore_w user large movie negative'):
        user_neg_div = review.find('div', class_='metascore_w user large movie negative')
        user_neg = user_neg_div.text
        # user_neg
        review_dict['user_score'].append(user_neg)
    if review.find('div', class_='metascore_w user large movie tbd'):
        user_tbd_div = review.find('div', class_='metascore_w user large movie tbd')
        user_tbd = user_tbd_div.text
        # user_tbd
        review_dict['user_score'].append(user_tbd)

movie_reviews = pd.DataFrame(review_dict)
movie_reviews = movie_reviews[movie_reviews['user_score'] != 'tbd']
movie_reviews = movie_reviews.iloc[:25]
# movie_reviews.reset_index(inplace=True)
movie_reviews['critic_score'] = movie_reviews.critic_score.astype(float)
movie_reviews['user_score'] = movie_reviews.user_score.astype(float)
movie_reviews['user_score'] = movie_reviews['user_score'] * 10

y = np.arange(25)
x = np.arange(0, 110, step=10)
fig, ax = plt.subplots()
width = 0.35
ax.barh(y + .2, movie_reviews['critic_score'], width, label='Critic Score')
ax.barh(y - .2, movie_reviews['user_score'], width, label='User Score')

ax.set_xlabel('Scores')
ax.set_title('Score Chart')
ax.legend()
plt.yticks(y, movie_reviews['name'])
plt.xticks(x)
# plt.figure(figsize=(20.0, 50.0))
# plt.tick_params(axis='y', which='major', labelsize=10)

st.title('Movie Reviews')
st.subheader('Critic Score and User Score')

# st.dataframe(movie_reviews)
AgGrid(movie_reviews)
st.pyplot(fig=fig)
