import urllib.parse

import requests
from bs4 import BeautifulSoup

from config import OMDB_API_KEY, TMDB_BEARER

HTML_PARSER = 'html.parser'

def fetch_similar_movies(letterboxd_url):
    """Attempt to fetch similar films from Letterboxd, with fallbacks.

    Tries related paths and parses poster grid; falls back to trending
    when nothing is found to avoid an empty UI block.
    """
    from imdb_scraper import fetch_trending_movies  # local import to avoid cycle

    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0 Safari/537.36'
        )
    }

    candidates = [
        f"{letterboxd_url.rstrip('/')}/related",
        f"{letterboxd_url.rstrip('/')}/similar",
    ]
    collected: list[dict] = []

    for url in candidates:
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code != 200:
                continue
            soup = BeautifulSoup(resp.text, HTML_PARSER)
            grid = soup.find('ul', class_='poster-list')
            if not grid:
                continue
            items = grid.find_all('li', class_='poster-container')
            for item in items[:6]:
                try:
                    film_poster = item.find('div', class_='film-poster')
                    if not film_poster:
                        continue
                    movie_title = film_poster.find('img')['alt']
                    omdb_url = (
                        f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
                    )
                    omdb_response = requests.get(omdb_url, timeout=10)
                    omdb_data = omdb_response.json() if omdb_response.ok else {}
                    poster_url = omdb_data.get('Poster') or ""
                    if not poster_url or poster_url == 'N/A':
                        poster_url = "https://placehold.co/300x450?text=No+Poster"
                    search_url = f"/{movie_title.replace(' ', '-')}"
                    collected.append({
                        'title': movie_title,
                        'url': search_url,
                        'poster': poster_url,
                    })
                except Exception:
                    continue
            if collected:
                break
        except Exception:
            continue

    if not collected:
        # Fallback to trending tiles to keep UI populated
        return fetch_trending_movies()[:6]
    return collected

def get_omdb_data(movie_title):
    """Fetches data from OMDb API."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    response = requests.get(url)
    return response.json()

def fetch_letterboxd_reviews(letterboxd_url):
    """Fetch multiple pages of reviews from a Letterboxd film page.

    Uses a real UA header, corrects the URL, and tries several selectors to
    adapt to minor DOM changes. Stops early when pages are empty.
    """
    headers = {
        'User-Agent': (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/124.0 Safari/537.36'
        )
    }
    base_url = letterboxd_url.rstrip('/')
    review_texts: list[str] = []

    def extract_reviews(soup: BeautifulSoup) -> list[str]:
        # Try a few different selectors that have appeared on Letterboxd
        selectors = [
            ('div', {'class': 'body-text'}),
            ('div', {'class': 'review'}),
            ('div', {'class': 'js-review-text'}),
            ('div', {'class': 'body-text -prose js-review-text'}),
        ]
        texts: list[str] = []
        for name, attrs in selectors:
            for el in soup.find_all(name, attrs=attrs):
                text = el.get_text(strip=True)
                if text and len(text) > 20:  # avoid tiny snippets
                    texts.append(text)
            if texts:
                break
        return texts

    # Try up to 6 pages
    for page in range(1, 7):
        paged_url = f"{base_url}/reviews/by/activity/page/{page}/"
        try:
            resp = requests.get(paged_url, headers=headers, timeout=10)
            if resp.status_code != 200:
                break
            soup = BeautifulSoup(resp.content, HTML_PARSER)
            texts = extract_reviews(soup)
            if not texts:
                # Try the vanilla reviews path once on first page
                if page == 1:
                    alt = f"{base_url}/reviews/"
                    resp2 = requests.get(alt, headers=headers, timeout=10)
                    if resp2.ok:
                        soup2 = BeautifulSoup(resp2.content, HTML_PARSER)
                        texts = extract_reviews(soup2)
                if not texts:
                    break
            review_texts.extend(texts)
        except Exception:
            break

    return review_texts


def scrape_user_reviews(movie_name):
    """Scrapes user reviews from Rotten Tomatoes for both movies (/m/) and TV shows (/t/)."""

    base_url = "https://www.rottentomatoes.com"
    slug = urllib.parse.quote(movie_name.lower().replace(" ", "_"))
    possible_paths = [f"/m/{slug}", f"/tv/{slug}"]
    headers = {"User-Agent": "Mozilla/5.0"}

    user_reviews = _fetch_rt_reviews_for_paths(base_url, possible_paths, headers)
    if user_reviews:
        return user_reviews

    # Retry with year if first attempt failed
    omdb_data = get_omdb_data(movie_name)
    movie_year = omdb_data.get('Year')
    if movie_year:
        paths_with_year = [f"{p}_{movie_year}" for p in possible_paths]
        return _fetch_rt_reviews_for_paths(base_url, paths_with_year, headers)
    return []


def _fetch_rt_reviews_for_paths(base_url: str, paths: list[str], headers: dict) -> list[str]:
    """Helper to fetch RT user reviews for a list of candidate paths."""
    all_reviews: list[str] = []
    for path in paths:
        full_url = f"{base_url}{path}/reviews?type=user"
        response = requests.get(full_url, headers=headers)
        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.content, HTML_PARSER)
        reviews = soup.find_all('div', class_='audience-review-row')
        for review in reviews:
            review_text = review.find('p', class_='audience-reviews__review js-review-text')
            if review_text:
                all_reviews.append(review_text.get_text(strip=True))
    return all_reviews


def get_tmdb_reviews(getmovie_name):
    """Fetch reviews from TMDB. Returns a list of review contents.

    Requires TMDB_BEARER to be set in the environment; otherwise returns [].
    """
    if not TMDB_BEARER:
        return []

    movie_name = getmovie_name.replace(" ", "%20")
    url = (
        "https://api.themoviedb.org/3/search/movie?query="
        f"{movie_name}&include_adult=false&language=en-US&page=1"
    )

    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TMDB_BEARER}",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json().get('results', [])
        if not result:
            return []
        movie_id = result[0]['id']

        url_for_review = (
            f"https://api.themoviedb.org/3/movie/{movie_id}/reviews?language=en-US&page=1"
        )
        response = requests.get(url_for_review, headers=headers, timeout=10)
        response.raise_for_status()
        results = response.json().get('results', [])
        return [r.get('content', '') for r in results if r.get('content')]
    except Exception:
        return []




def fetch_movie_reviews_and_details(movie_title, letterboxd_url):
    """Combines OMDb movie details with Letterboxd and Rotten Tomatoes reviews."""

    omdb_data = get_omdb_data(movie_title)
    print(omdb_data)

    review_texts = fetch_letterboxd_reviews(letterboxd_url)

    # Also fetch Rotten Tomatoes reviews and combine
    rt_reviews = scrape_user_reviews(movie_title)
    review_texts.extend(rt_reviews)

    # Optionally include TMDB reviews if token configured
    # tmdb_reviews = get_tmdb_reviews(movie_title)
    # review_texts.extend(tmdb_reviews)

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
