import pickle
import streamlit as st
import requests

# Function to fetch poster
def fetch_poster(place_id, client_id):
    url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': place_id,
        'client_id': client_id,
        'per_page': 1  # Adjust as needed
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'results' in data and data['results']:
        return data['results'][0]['urls']['regular']
    else:
        return None

# Function to recommend places
def recommend(place):
    index = places[places['City'] == place].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_places = []
    for i in distances[1:6]:
        recommended_place_id = places.iloc[i[0]]['City']
        unsplash_client_id='9NYhYGvMJhE-tzqNlsNLEKyyj2qHbOaN7K_jlbz8SyU'

        poster_url = fetch_poster(recommended_place_id, unsplash_client_id)
        recommended_places.append((recommended_place_id, poster_url))
    return recommended_places

# Load data
places = pickle.load(open('artifacts\.ipynb_checkpoints\place_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts\.ipynb_checkpoints\similarity.pkl', 'rb'))

# Streamlit UI
st.title("Tour Recommendation System Using Machine Learning")

# Select place
selected_place = st.selectbox('Select a city to get recommendations:', places['City'].values)

# Button to show recommendations
if st.button('Show Recommendations'):
    recommended_places = recommend(selected_place)
    st.subheader('Recommended Places:')
    for place, poster_url in recommended_places:
        if poster_url:
            st.image(poster_url, caption=place, use_column_width=True)
        else:
            st.write(place)
