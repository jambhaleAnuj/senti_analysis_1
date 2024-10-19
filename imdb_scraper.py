from imdb import IMDb
import re
import requests

# Replace with your OMDb API key
OMDB_API_KEY = '36650a58'

def extract_imdb_id(imdb_url):
    """Extracts the IMDb ID from the URL."""
    match = re.search(r'tt(\d+)', imdb_url)
    if match:
        return match.group(1)
    return None

def get_omdb_data(movie_title):
    """Fetches data from OMDb API."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()

def fetch_imdb_reviews(imdb_url):
    """Fetches IMDb reviews using IMDbPY."""
    imdb_id = extract_imdb_id(imdb_url)
    
    if not imdb_id:
        return [], {}

    ia = IMDb()
    
    try:
        movie = ia.get_movie(imdb_id)
        reviews = ia.get_movie_reviews(imdb_id)
        user_reviews = reviews['data']['reviews']
        review_texts = [review['content'] for review in user_reviews]

        # Fetch additional movie details from OMDb
        omdb_data = get_omdb_data(movie['title'])
        
        movie_details = {
            'title': movie['title'],
            'year': movie.get('year'),
            'rating': omdb_data.get('imdbRating', 'N/A'),  # Get IMDb rating from OMDb
            'genres': omdb_data.get('Genre', 'N/A'),      # Get genres from OMDb
            'box_office': omdb_data.get('BoxOffice', 'N/A'),  # Get box office info
            'release_date': omdb_data.get('Released', 'N/A'),  # Get release date
            'plot' : omdb_data.get('Plot','N/A'),
            'actor' : omdb_data.get('Actors','N/A'),
            'director' : omdb_data.get('Director','N/A'),
            'poster': omdb_data.get('Poster', 'N/A'),
            'language':omdb_data.get('Language','N/A'),
            'country': omdb_data.get('Country','N/A'),
            'awards' : omdb_data.get('Awards','N/A'),
            'writer' : omdb_data.get('Writer','N/A')
        }
        print(movie_details)
        
        
        return review_texts, movie_details

    except Exception as e:
        print(f"Error fetching IMDb data: {e}")
        return [], {}
