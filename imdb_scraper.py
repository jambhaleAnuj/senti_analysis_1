import requests
from bs4 import BeautifulSoup
import re

# OMDb API Key
OMDB_API_KEY = '36650a58'


def get_omdb_data(movie_title):
    """Fetches data from OMDb API."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()

def fetch_letterboxd_reviews(letterboxd_url):
    """Fetches reviews from Letterboxd."""
    response = requests.get(letterboxd_url)
    if response.status_code != 200:
        return []
    
    season_page = BeautifulSoup(response.content, 'html.parser')
    reviews = season_page.find_all('div', class_='body-text -prose collapsible-text')
    
    review_texts = []
    for review in reviews:
        review_text = review.get_text(strip=True)
        review_texts.append(review_text)
    
    return review_texts

def fetch_movie_reviews_and_details(movie_title, letterboxd_url):
    
    """Combines OMDb movie details with Letterboxd reviews."""
    # Fetch movie details from OMDb
    omdb_data = get_omdb_data(movie_title)
    
    # Fetch reviews from Letterboxd
    review_texts = fetch_letterboxd_reviews(letterboxd_url)

    # Organize movie details
    movie_details = {
        'title': omdb_data.get('Title', 'N/A'),
        'year': omdb_data.get('Year', 'N/A'),
        'rating': omdb_data.get('imdbRating', 'N/A'),
        'genres': omdb_data.get('Genre', 'N/A'),
        'box_office': omdb_data.get('BoxOffice', 'N/A'),
        'release_date': omdb_data.get('Released', 'N/A'),
        'plot': omdb_data.get('Plot', 'N/A'),
        'actor': omdb_data.get('Actors', 'N/A'),
        'director': omdb_data.get('Director', 'N/A'),
        'poster': omdb_data.get('Poster', 'N/A'),
        'language': omdb_data.get('Language', 'N/A'),
        'country': omdb_data.get('Country', 'N/A'),
        'awards': omdb_data.get('Awards', 'N/A'),
        'writer': omdb_data.get('Writer', 'N/A')
    }

    return review_texts, movie_details
