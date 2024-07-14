import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
   url = "https://api.themoviedb.org/3/movie/{}?api_key=a51527ec807d3f1c0f5a7b49f05238aa".format(movie_id)
   response = requests.get(url)
   data = response.json()
   # st.text(data) --> to print the data
   return "https://image.tmdb.org/t/p/original/" + data['poster_path']


def recommend(movie):
   movie_idx = movies[movies['title'] == movie].index[0]
   distances = similarity[movie_idx]
   movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1]) [1:6]
   
   recommended_movies = []
   recommended_movies_posters = []
   for i in movies_list:
      movie_id = movies.iloc[i[0]].movie_id

      recommended_movies.append(movies.iloc[i[0]].title)
      # fetch poster from api
      recommended_movies_posters.append(fetch_poster(movie_id))
   return recommended_movies, recommended_movies_posters


# movies_list = pickle.load(open('movies.pkl', 'rb'))
# movies_list = movies_list['title'].values

movies_dicts = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dicts)

similarity = pickle.load(open('similar_movies.pkl', 'rb'))



st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
   'How would you like to watch ?',
   (movies['title'].values)
)

if st.button('Recommend'):
   names, posters = recommend(selected_movie_name)
   
   col1, col2, col3, col4, col5 = st.columns(5)

   with col1:
      st.text(names[0])
      st.image(posters[0])

   with col2:
      st.text(names[1])
      st.image(posters[1])

   with col3:
      st.text(names[2])
      st.image(posters[2])

   with col4:
      st.text(names[3])
      st.image(posters[3])

   with col5:
      st.text(names[4])
      st.image(posters[4])

st.markdown(
    """
    <style>
    .reportview-container {
        background: url("https://www.google.com/url?sa=i&url=https%3A%2F%2Fpngtree.com%2Ffree-backgrounds-photos%2Fblack-film&psig=AOvVaw3Nji_ppXKVjgw3h09o1SWC&ust=1720616627330000&source=images&cd=vfe&opi=89978449&ved=0CBEQjRxqFwoTCPDaocyCmocDFQAAAAAdAAAAABAE")
    }
    </style>
    """,
    unsafe_allow_html=True
)