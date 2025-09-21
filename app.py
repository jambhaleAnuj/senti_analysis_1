"""Flask application entrypoint.

This module handles routing, orchestrates data fetching, sentiment analysis,
and visualization assembly. Cleaned from large historical commented code blocks
for clarity and maintainability.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

import plotly.graph_objects as go
import requests
from flask import (
    Flask,
    abort,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from plotly.utils import PlotlyJSONEncoder

from cache import get as cache_get
from cache import put as cache_put
from config import FLASK_DEBUG, OMDB_API_KEY
from imdb_scraper import fetch_movie_reviews_and_details, fetch_trending_movies
from sentiment_analysis import (
    analyze_sentiment,
    analyze_sentiment_vader,
    create_visualizations,
    generate_word_cloud,
    plot_genre_distribution,
    plot_word_frequency,
)
from summarizer import generate_summary
from youtube_scraper import get_trailer_comments

app = Flask(__name__)

# Common literals
INDEX_TEMPLATE = 'index.html'
ERROR_NO_REVIEWS = "No reviews found for this movie."

FALLBACK_TRENDING = [
    {
        'title': 'A Minecraft Movie',
        'link': 'a-minecraft-movie',
        'image': 'https://a.ltrbxd.com/resized/film-poster/8/5/4/6/9/1/854691-a-minecraft-movie-0-1000-0-1500-crop.jpg?v=074e7fed9e'
    },
    {
        'title': 'warfare',
        'link': 'Warfare',
        'image': 'https://a.ltrbxd.com/resized/film-poster/1/1/2/4/7/0/1/1124701-warfare-0-2000-0-3000-crop.jpg?v=f379233a1b'
    },
    {
        'title': 'Drop',
        'link': 'drop',
        'image': 'https://m.media-amazon.com/images/M/MV5BOWUyOTNlMjItNWUyZC00ZGJiLTg3MDMtODJmMGQyMGY3NzU3XkEyXkFqcGc@._V1_SX300.jpg'
    },
    {
        'title': 'The Last of Us',
        'link': 'the-last-of-us',
        'image': 'https://m.media-amazon.com/images/M/MV5BYWI3ODJlMzktY2U5NC00ZjdlLWE1MGItNWQxZDk3NWNjN2RhXkEyXkFqcGc@._V1_SX300.jpg'
    },
    {
        'title': 'G20',
        'link': 'G20',
        'image': 'https://a.ltrbxd.com/resized/film-poster/9/4/3/3/8/5/943385-g20-0-1000-0-1500-crop.jpg?v=4eb0e8db3c'
    },
    {
        'title': 'Mickey 17',
        'link': 'mickey-17',
        'image': 'https://a.ltrbxd.com/resized/film-poster/6/2/0/2/8/1/620281-mickey-17-0-1000-0-1500-crop.jpg?v=93e4d2af6d'
    },
    {
        'title': 'Novocaine',
        'link': 'novocaine',
        'image': 'https://a.ltrbxd.com/resized/film-poster/1/0/8/1/0/1/7/1081017-novocaine-2025-0-1000-0-1500-crop.jpg?v=bf4021de18'
    },
    {
        'title': 'Captain America: Brave New World',
        'link': 'Captain-America-Brave-New-World',
        'image': 'https://a.ltrbxd.com/resized/film-poster/7/3/8/2/9/2/738292-captain-america-brave-new-world-0-1000-0-1500-crop.jpg?v=97dff5b720'
    },
    {
        'title': 'Death of a Unicorn',
        'link': 'Death-of-a-Unicorn',
        'image': 'https://a.ltrbxd.com/resized/film-poster/1/0/3/9/7/3/6/1039736-death-of-a-unicorn-0-1000-0-1500-crop.jpg?v=973751852e'
    },
    {
        'title': 'The electric state',
        'link': 'The-electric-state',
        'image': 'https://a.ltrbxd.com/resized/film-poster/6/9/6/7/2/5/696725-the-electric-state-0-1000-0-1500-crop.jpg?v=0d8eae00e9'
    },
    {
        'title': 'The Batman',
        'link': 'the-Batman',
        'image': 'https://a.ltrbxd.com/resized/film-poster/3/4/8/9/1/4/348914-the-batman-0-1000-0-1500-crop.jpg?v=ec12a8b7ce'
    },
    {
        'title': 'Adolescence',
        'link': 'Adolescence',
        'image': 'https://a.ltrbxd.com/resized/film-poster/1/3/2/6/8/2/8/1326828-adolescence-2025-0-1000-0-1500-crop.jpg?v=dde7c2d9f0'
    },
    # Add more fallback movies as needed
]

def _select_trending_movies() -> List[Dict[str, str]]:
    """Return trending movies falling back to static list if API fails.

    For now always uses fallback if fetch returns empty or None.
    """
    api_movies = fetch_trending_movies()
    if not api_movies:
        return FALLBACK_TRENDING
    return api_movies


def _perform_full_analysis(
    reviews: List[str],
    movie_details: Dict[str, Any],
    similar_movies: List[Dict[str, Any]],
):
    """Run sentiment workflow and return redirect response parameters.

    Returns a dictionary suitable to pass into url_for('results', **params)
    (temporary approach until server-side session/cache is implemented).
    """
    (
        sentiments,
        positive_reviews,
        neutral_reviews,
        negative_reviews,
        polarity_scores,
        positive_keywords,
        negative_keywords,
    ) = analyze_sentiment(reviews)

    vader_counts, _vader_detail = analyze_sentiment_vader(reviews)

    # Side-effect visual assets
    generate_word_cloud(reviews)
    create_visualizations(sentiments, polarity_scores, movie_details)

    return {
        "movie": movie_details["title"],
        "year": movie_details["year"],
        "rating": movie_details["rating"],
        "genres": movie_details["genres"],
        "plot": movie_details["plot"],
        "actors": movie_details["actor"],
        "poster": movie_details["poster"],
        "language": movie_details["language"],
        "country": movie_details["country"],
        "writer": movie_details["writer"],
        "awards": movie_details["awards"],
        "director": movie_details["director"],
        "box_office": movie_details["box_office"],
        "release_date": movie_details["release_date"],
        "positive": len(positive_reviews),
        "neutral": len(neutral_reviews),
        "negative": len(negative_reviews),
        "total": len(reviews),
        "rev": json.dumps(reviews),
        "positive_keywords": json.dumps(dict(positive_keywords)),
        "negative_keywords": json.dumps(dict(negative_keywords)),
        "similar_movies": json.dumps(similar_movies),
        # VADER counts
        "vader_positive": vader_counts.get("positive", 0),
        "vader_neutral": vader_counts.get("neutral", 0),
        "vader_negative": vader_counts.get("negative", 0),
    }


def _fetch_and_analyze(movie_name: str) -> Dict[str, Any] | None:
    """Fetch reviews/details and run analysis pipeline, returning redirect params.

    Returns None if no reviews were found.
    """
    letterboxd_url = movie_name.replace(" ", "-").lower()
    letterboxd_full_url = f"https://letterboxd.com/film/{letterboxd_url}/"
    reviews, movie_details, similar_movies = fetch_movie_reviews_and_details(
        movie_name, letterboxd_full_url
    )
    if not reviews:
        return None
    return _perform_full_analysis(reviews, movie_details, similar_movies)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Unified index route (search + similar movie follow-up)."""
    trending_movies = _select_trending_movies()
    if request.method == 'POST':
        movie_name = request.form.get('letterboxd_url', '').strip()
        if movie_name:
            params = _fetch_and_analyze(movie_name)
            if params is None:
                return render_template(
                    INDEX_TEMPLATE,
                    error=ERROR_NO_REVIEWS,
                    trending_movies=trending_movies,
                )
            # store in cache
            cache_key = cache_put(params)
            return redirect(url_for('results_cached', key=cache_key))
    else:  # GET
        similar_clicked = request.args.get('letterboxd_url')
        if similar_clicked:
            params = _fetch_and_analyze(similar_clicked)
            if params is None:
                return render_template(
                    INDEX_TEMPLATE,
                    error=ERROR_NO_REVIEWS,
                    trending_movies=trending_movies,
                )
            return redirect(url_for('results', **params))
    return render_template(INDEX_TEMPLATE, trending_movies=trending_movies)


@app.route('/analyze', methods=['POST'])
def analyze():
    """Dedicated POST endpoint (AJAX or form) to analyze a movie title.

    Expects form field 'movie_title'. Returns redirect to cached results.
    """
    movie_name = request.form.get('movie_title', '').strip()
    if not movie_name:
        return redirect(url_for('index'))
    params = _fetch_and_analyze(movie_name)
    if params is None:
        return render_template(INDEX_TEMPLATE, error=ERROR_NO_REVIEWS)
    cache_key = cache_put(params)
    return redirect(url_for('results_cached', key=cache_key))


    # (Removed legacy duplicate index implementation.)



def _build_youtube_sentiment(movie: str) -> Dict[str, Any]:
    """Fetch trailer comments and build sentiment visualization JSON objects."""
    trailer_comments = get_trailer_comments(movie)
    if trailer_comments:
        yt_sentiments, *_rest = analyze_sentiment([c['text'] for c in trailer_comments])
    else:
        # empty fallback
        yt_sentiments = {"positive": 0, "neutral": 0, "negative": 0}

    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [yt_sentiments['positive'], yt_sentiments['neutral'], yt_sentiments['negative']]
    fig_pie_yt = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=sizes,
                hoverinfo='label+percent',
                textinfo='percent',
            )
        ]
    )
    pie_json_yt = json.dumps(fig_pie_yt, cls=PlotlyJSONEncoder)
    fig_bar_yt = go.Figure(
        data=[go.Bar(x=labels, y=sizes, marker={"color": ['green', 'gray', 'red']})]
    )
    bar_json_yt = json.dumps(fig_bar_yt, cls=PlotlyJSONEncoder)
    word_freq_yt = (
    plot_word_frequency([c['text'] for c in trailer_comments], {'title': movie})
        if trailer_comments
        else None
    )
    word_freq_json_yt = json.dumps(word_freq_yt, cls=PlotlyJSONEncoder) if word_freq_yt else None
    return {
        "pie_chart_yt": pie_json_yt,
        "bar_chart_yt": bar_json_yt,
        "word_freq_plot_yt": word_freq_json_yt,
    }


@app.route('/results')
def results():  # backward compatibility (legacy query param path)
    try:
        # Basic scalar params
        movie = request.args.get('movie', '')
        year = request.args.get('year')
        rating = request.args.get('rating')
        plot = request.args.get('plot')
        director = request.args.get('director')
        poster = request.args.get('poster')
        language = request.args.get('language')
        writer = request.args.get('writer')
        awards = request.args.get('awards')
        country = request.args.get('country')
        genres = request.args.get('genres')
        box_office = request.args.get('box_office')
        release_date = request.args.get('release_date')
        actors = request.args.get('actors')

        positive = int(request.args.get('positive', 0))
        neutral = int(request.args.get('neutral', 0))
        negative = int(request.args.get('negative', 0))
        total = int(request.args.get('total', 0))

        vader_positive = int(request.args.get('vader_positive', 0))
        vader_neutral = int(request.args.get('vader_neutral', 0))
        vader_negative = int(request.args.get('vader_negative', 0))

        positive_keywords = json.loads(request.args.get('positive_keywords', '{}'))
        negative_keywords = json.loads(request.args.get('negative_keywords', '{}'))
        positive_keywords = list(positive_keywords.items())
        negative_keywords = list(negative_keywords.items())

        similar_movies = json.loads(request.args.get('similar_movies', '[]'))
        reviews = json.loads(request.args.get('rev', '[]'))

        # Build YouTube charts
        yt_payload = (
            _build_youtube_sentiment(movie)
            if movie
            else {"pie_chart_yt": None, "bar_chart_yt": None, "word_freq_plot_yt": None}
        )

        # Genre distribution
        genre_fig = plot_genre_distribution(genres) if genres else None
        genre_plot_json = json.dumps(genre_fig, cls=PlotlyJSONEncoder) if genre_fig else None

        # Word frequency for reviews (overall)
        word_freq_plot_html = (
            plot_word_frequency(reviews, {"title": movie}) if reviews else None
        )
        word_freq_plot_json = (
            json.dumps(word_freq_plot_html, cls=PlotlyJSONEncoder)
            if word_freq_plot_html
            else None
        )

        fig_pie, fig_bar, fig_hist = create_visualizations(
            {"positive": positive, "neutral": neutral, "negative": negative},
            [positive, neutral, negative],
            {"title": movie},
        )
        pie_json = json.dumps(fig_pie, cls=PlotlyJSONEncoder)
        bar_json = json.dumps(fig_bar, cls=PlotlyJSONEncoder)
        hist_json = json.dumps(fig_hist, cls=PlotlyJSONEncoder)

        summary = (
            generate_summary(
                movie,
                plot,
                {"positive": positive, "neutral": neutral, "negative": negative},
            )
            if movie
            else None
        )

        return render_template(
            'results.html',
            movie=movie,
            plot=plot,
            actors=actors,
            director=director,
            poster=poster,
            language=language,
            country=country,
            writer=writer,
            awards=awards,
            year=year,
            rating=rating,
            genres=genres,
            box_office=box_office,
            release_date=release_date,
            positive=positive,
            neutral=neutral,
            negative=negative,
            total=total,
            vader_positive=vader_positive,
            vader_neutral=vader_neutral,
            vader_negative=vader_negative,
            positive_keywords=positive_keywords,
            negative_keywords=negative_keywords,
            similar_movies=similar_movies,
            pie_chart=pie_json,
            bar_chart=bar_json,
            hist_chart=hist_json,
            word_freq_plot=word_freq_plot_json,
            genre_plot_json=genre_plot_json,
            **yt_payload,
            summary=summary,
        )
    except Exception as e:  # pragma: no cover - defensive
        return render_template('error.html', error=str(e))


@app.route('/results/<key>')
def results_cached(key: str):  # noqa: C901
    data = cache_get(key)
    if not data:
        abort(404)
    try:
        # Extract what we stored originally
        movie = data.get('movie')
        plot = data.get('plot')
        year = data.get('year')
        rating = data.get('rating')
        genres = data.get('genres')
        director = data.get('director')
        actors = data.get('actors')
        poster = data.get('poster')
        language = data.get('language')
        country = data.get('country')
        writer = data.get('writer')
        awards = data.get('awards')
        box_office = data.get('box_office')
        release_date = data.get('release_date')
        positive = data.get('positive', 0)
        neutral = data.get('neutral', 0)
        negative = data.get('negative', 0)
        total = data.get('total', 0)
        vader_positive = data.get('vader_positive', 0)
        vader_neutral = data.get('vader_neutral', 0)
        vader_negative = data.get('vader_negative', 0)
        reviews = (
            json.loads(data.get('rev', '[]'))
            if isinstance(data.get('rev'), str)
            else data.get('rev', [])
        )
        positive_keywords = (
            list(json.loads(data.get('positive_keywords', '{}')).items())
            if isinstance(data.get('positive_keywords'), str)
            else data.get('positive_keywords', [])
        )
        negative_keywords = (
            list(json.loads(data.get('negative_keywords', '{}')).items())
            if isinstance(data.get('negative_keywords'), str)
            else data.get('negative_keywords', [])
        )
        similar_movies = (
            json.loads(data.get('similar_movies', '[]'))
            if isinstance(data.get('similar_movies'), str)
            else data.get('similar_movies', [])
        )

        # Rebuild charts on demand (lightweight) rather than storing them
        fig_pie, fig_bar, fig_hist = create_visualizations(
            {"positive": positive, "neutral": neutral, "negative": negative},
            [positive, neutral, negative],
            {"title": movie},
        )
        pie_json = json.dumps(fig_pie, cls=PlotlyJSONEncoder)
        bar_json = json.dumps(fig_bar, cls=PlotlyJSONEncoder)
        hist_json = json.dumps(fig_hist, cls=PlotlyJSONEncoder)
        genre_plot_json = None
        if genres:
            genre_fig = plot_genre_distribution(genres)
            genre_plot_json = json.dumps(genre_fig, cls=PlotlyJSONEncoder)
        word_freq_plot_json = None
        if reviews:
            wf = plot_word_frequency(reviews, {"title": movie})
            word_freq_plot_json = json.dumps(wf, cls=PlotlyJSONEncoder)
        yt_payload = (
            _build_youtube_sentiment(movie)
            if movie
            else {"pie_chart_yt": None, "bar_chart_yt": None, "word_freq_plot_yt": None}
        )
        summary = (
            generate_summary(
                movie,
                plot,
                {"positive": positive, "neutral": neutral, "negative": negative},
            )
            if movie
            else None
        )

        return render_template(
            'results.html',
            movie=movie,
            plot=plot,
            actors=actors,
            director=director,
            poster=poster,
            language=language,
            country=country,
            writer=writer,
            awards=awards,
            year=year,
            rating=rating,
            genres=genres,
            box_office=box_office,
            release_date=release_date,
            positive=positive,
            neutral=neutral,
            negative=negative,
            total=total,
            vader_positive=vader_positive,
            vader_neutral=vader_neutral,
            vader_negative=vader_negative,
            positive_keywords=positive_keywords,
            negative_keywords=negative_keywords,
            similar_movies=similar_movies,
            pie_chart=pie_json,
            bar_chart=bar_json,
            hist_chart=hist_json,
            word_freq_plot=word_freq_plot_json,
            genre_plot_json=genre_plot_json,
            **yt_payload,
            summary=summary,
        )
    except Exception as e:  # pragma: no cover
        return render_template('error.html', error=str(e))



@app.route('/get_movie_suggestions', methods=['GET'])
def get_movie_suggestions():
    query = request.args.get('query', '').strip()

    # If the query is less than 3 characters, don't make an API call
    if len(query) < 3:
        return jsonify(suggestions=[])

    # Fetch suggestions from OMDb API
    omdb_url = f"http://www.omdbapi.com/?s={query}&apikey={OMDB_API_KEY}"
    response = requests.get(omdb_url)


    # If the response is OK and there are search results
    if response.status_code == 200:
        data = response.json()
        if data.get('Response') == 'True':
            # Extract movie titles and return them as suggestions
            suggestions = [{'title': movie['Title']} for movie in data.get('Search', [])]
            return jsonify(suggestions=suggestions)

    return jsonify(suggestions=[])

if __name__ == '__main__':
    app.run(debug=FLASK_DEBUG)
