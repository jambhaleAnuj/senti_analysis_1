import json
import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
from dotenv import load_dotenv
import os

# load_dotenv()
# TMDB_API = os.getenv("TMDB_API")


OMDB_API_KEY = '36650a58'

def fetch_similar_movies(letterboxd_url):
    similar_movies = []

    try:
        similar_url = f"{letterboxd_url}/similar"
        headers = {
            'User -Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        response = requests.get(similar_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        similar_grid = soup.find('ul', class_='poster-list')
        if similar_grid:
            movie_items = similar_grid.find_all('li', class_='poster-container')

            for item in movie_items[:6]:
                try:
                    film_poster = item.find('div', class_='film-poster')
                    if film_poster:
                        movie_title = film_poster.find('img')['alt']
                        movie_url = film_poster['data-target-link']

                        omdb_url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
                        omdb_response = requests.get(omdb_url)
                        omdb_data = omdb_response.json()

                        poster_url = omdb_data.get('Poster', 'N/A')
                        if poster_url == 'N/A':
                            poster_url = "path/to/default/poster.jpg"

                        search_url = f"/{movie_title.replace(' ','-')}"

                        similar_movies.append({
                            'title': movie_title,
                            'url': search_url,
                            'poster': poster_url,
                        })

                except Exception as e:
                    print(f"Error processing similar movie: {e}")
                    continue

    except Exception as e:
        print(f"Error fetching similar movies: {e}")

    return similar_movies

def get_omdb_data(movie_title):
    """Fetches data from OMDb API."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()

def fetch_letterboxd_reviews(letterboxd_url):
    """Fetches multiple pages of reviews from Letterboxd review pages."""
    base_url = letterboxd_url.rstrip('/')
    review_texts = []

    # Try to fetch reviews from up to 10 pages
    for page in range(1, 5):  # You can change 11 to any desired page count limit
        paged_url = f"{base_url}//reviews/by/activity/page/{page}/"
        print(f"Fetching: {paged_url}")
        response = requests.get(paged_url)
        if response.status_code != 200:
            print(f"Page {page} failed to load.")
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', class_='body-text -prose js-review-body js-collapsible-text')

        if not reviews:
            # No more reviews found, stop paginating
            print(f"No reviews found on page {page}, stopping.")
            break

        for review in reviews:
            review_text = review.get_text(strip=True)
            review_texts.append(review_text)

    return review_texts


def scrape_user_reviews(movie_name):
    """Scrapes user reviews from Rotten Tomatoes for both movies (/m/) and TV shows (/t/)."""
    
    base_url = "https://www.rottentomatoes.com"
    slug = urllib.parse.quote(movie_name.lower().replace(" ", "_"))

    possible_paths = [f"/m/{slug}", f"/tv/{slug}"]
    user_reviews = []

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    # First attempt: try both paths (movie and TV show)
    for path in possible_paths:
        full_url = f"{base_url}{path}/reviews?type=user"
        print(f"Trying: {full_url}")
        response = requests.get(full_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            reviews = soup.find_all('div', class_='audience-review-row')

            for review in reviews:
                review_text = review.find('p', class_='audience-reviews__review js-review-text')
                if review_text:
                    user_reviews.append(review_text.get_text(strip=True))

    # If no reviews are found, attempt to retry with the movie year
    if not user_reviews:
        # You would need a function to get movie details, like 'get_omdb_data()'
        omdb_data = get_omdb_data(movie_name)  # Assume this function gets the movie year
        movie_year = omdb_data.get('Year')

        if movie_year:
            print(f"Movie year found: {movie_year}")
            for path in possible_paths:
                # Try with the year appended to the path for both movie and TV show
                full_url = f"{base_url}{path}_{movie_year}/reviews?type=user"
                print(f"Trying with year: {full_url}")
                response = requests.get(full_url, headers=headers)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    reviews = soup.find_all('div', class_='audience-review-row')

                    for review in reviews:
                        review_text = review.find('p', class_='audience-reviews__review js-review-text')
                        if review_text:
                            user_reviews.append(review_text.get_text(strip=True))

        else:
            print("No movie year found. Could not retry with year.")

    # If no reviews are found even after retrying with the year
    if not user_reviews:
        print(f"No reviews found for {movie_name} on Rotten Tomatoes.")
    # print("ROTTENT TOMATOES: \n",user_reviews)
    return user_reviews


def get_tmdb_reviews(getmovie_name):
    movie_name = getmovie_name
    movie_name.replace(" ","%20")
    url = f"https://api.themoviedb.org/3/search/movie?query={movie_name}&include_adult=false&language=en-US&page=1"

    headers = {
        "accept": "application/json",
        f"Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzMDExMTgzMjU1Njc5MWM2OThhMzcwYjdlNmYyMzc4NCIsIm5iZiI6MTc0NTE2MTY0Ny44MDA5OTk5LCJzdWIiOiI2ODA1MGRhZjZlMWE3NjllODFlZTI1MmUiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.wp7NbWIr8Itm1ZCmVeVIq6JcVZiwnhmencqG5GE-N_o"
    }

    response = requests.get(url, headers=headers)
    result = response.json().get('results')

    movie_id = result[0]['id']
    print(movie_id)


    url_for_review = f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"

    response = requests.get(url_for_review, headers=headers)
    result = response.json().get('results')
    tmdb_reviews = result[0]['content']
    print(tmdb_reviews)
    return tmdb_reviews




def fetch_movie_reviews_and_details(movie_title, letterboxd_url):
    """Combines OMDb movie details with Letterboxd and Rotten Tomatoes reviews."""

    omdb_data = get_omdb_data(movie_title)
    print(omdb_data)

    review_texts = fetch_letterboxd_reviews(letterboxd_url)

    # Also fetch Rotten Tomatoes reviews and combine
    rt_reviews = scrape_user_reviews(movie_title)
    review_texts.extend(rt_reviews)

    tmdb_review = get_tmdb_reviews(movie_title)
    print(tmdb_review)
    review_texts.extend(tmdb_review)
    print("Added TMDB reviews")
    # print(review_texts)

    similar_movies = fetch_similar_movies(letterboxd_url)

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

    return review_texts, movie_details, similar_movies

trend_url = "https://letterboxd.com/films/ajax/popular/this/week/?esiAllowFilters=true"
BASE_URL = 'http://www.omdbapi.com/'

def get_poster_from_omdb(title):
    params = {
        't': title,
        'apikey': OMDB_API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()

        if data.get('Response') == 'True':
            return data.get('Poster', 'No poster found')
        else:
            return 'No poster found'
    else:
        return 'Error fetching data from OMDB'

def fetch_trending_movies():
    response = requests.get(trend_url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        films = soup.find_all('div', class_='poster')

        trending_movies = []
        count = 0
        for film in films:
            if count >= 12:
                break

            title = film.find('img')['alt'] if film.find('img') else 'No title found'
            link = title.lower().replace(' ', '-')
            omdb_poster_url = get_poster_from_omdb(title)

            movie_data = {
                'title': title,
                'link': link,
                'image': omdb_poster_url
            }

            trending_movies.append(movie_data)
            count += 1

        return trending_movies
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return []
