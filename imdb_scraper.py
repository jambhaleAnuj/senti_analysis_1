from imdb import IMDb
import re

# Function to extract IMDb ID from URL
def extract_imdb_id(imdb_url):
    match = re.search(r'tt(\d+)', imdb_url)
    if match:
        return match.group(1)
    return None

# Function to fetch IMDb reviews using IMDbPY
def fetch_imdb_reviews(imdb_url):
    imdb_id = extract_imdb_id(imdb_url)
    
    if not imdb_id:
        return [], {}

    ia = IMDb()
    
    try:
        movie = ia.get_movie(imdb_id)
        reviews = ia.get_movie_reviews(imdb_id)
        user_reviews = reviews['data']['reviews']
        review_texts = [review['content'] for review in user_reviews]

        movie_details = {
            'title': movie['title'],
            'year': movie.get('year'),
            'rating': movie.get('rating'),
            'genres': movie.get('genres')
        }
        
        return review_texts, movie_details

    except Exception as e:
        print(f"Error fetching IMDb data: {e}")
        return [], {}
