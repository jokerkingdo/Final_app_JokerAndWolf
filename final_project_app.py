import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

plt.style.use('seaborn')

# read the dataset
df_songs = pd.read_csv('top10s.csv')

# set title and subtitle(what problem we discuss)
st.title('Popular songs app by Weihao Jiang and Shuaipeng Liu')
st.subheader('we discuss the relationship between popularity and bpm based on different music type and year.')
st.subheader('also discuss relationship between liveness and bpm based on different type and year')

# bpm selection
bpm_filter = st.slider('Please choose a bpm:', 0, 201, 70)
bpm_choose = st.radio('Choose more or less than that bpm:', ['More than', 'Less than'])

# sidebar
#   choose music types
type_filter = st.sidebar.multiselect(
    'Choose your wanted music type',
    df_songs.top_genre.unique(),
    df_songs.top_genre.unique()
)

#   choose the year the song awarded
form = st.sidebar.form("Input a year between 2010 and 2019")
year_filter = form.text_input('Input a year between 2010 and 2019 (enter ALL to reset)', 'ALL')
form.form_submit_button("Apply")

# apply those selection
if bpm_choose == 'More than':
    df_songs = df_songs[df_songs.bpm >= bpm_filter]
else:
    df_songs = df_songs[df_songs.bpm <= bpm_filter]

df_songs = df_songs[df_songs.top_genre.isin(type_filter)]

if year_filter != 'ALL':
    df_songs = df_songs[df_songs.year == int(year_filter)]

# show the plots
st.subheader('According to the bpm, which artist\'s songs has most popularity(Top 30 only):')
fig0, ax0 = plt.subplots(figsize=(10, 5))
df_songs.groupby('artist').pops.sum().sort_values(ascending = False).head(30).plot.bar()
plt.xticks(rotation=90)
st.pyplot(fig0)
st.subheader('histogram about popularity and bpm')
fig1, ax1 = plt.subplots(figsize=(10, 5))
df_songs.pops.hist(bins = 30)
st.pyplot(fig1)
st.subheader('boxgram of liveness according to bpm')
fig2, ax2 = plt.subplots(figsize=(10, 5))
df_songs.live.plot.box()
st.pyplot(fig2)
