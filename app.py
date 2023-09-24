import streamlit as st
import pickle
import pandas as pd
import requests

# function to fetch poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?append_to_response=string&language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJkZjdjMzI5YzI5YzVhZDQyYmY5OWY2NmEwZTBkNjcwZSIsInN1YiI6IjY1MTAzZmYxNmY1M2UxMGFhM2MwODQ2MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.KpxKu5DUQAMhry_xIQq5wPwi2i2ruk8jXRMD7VMq6dY"
    }

    response = requests.get(url.format(movie_id), headers=headers)
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']

# function to recommend similar movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key = lambda x:x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = [] 
    for i in movie_list:
       movie_id = movies.iloc[i[0]].movie_id

       recommended_movies.append(movies.iloc[i[0]].title)
       recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

#loading data from pickle files
movies_list = pickle.load(open('movies.pkl','rb'))
movies = pd.DataFrame(movies_list)
movies_list = movies_list['title'].values

similarity = pickle.load(open('similarity.pkl','rb'))              

#title for the app
st.title("Movie Recommender System")

#creating the select box for the app
selected_movie_name = st.selectbox(
"Choose a movie for which you want to find similar movies?",
(movies_list),
)

# clreating layout and content of the app
if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)
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

