import os
from collections import Counter
from typing import Dict, List

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import nltk
import plotly.express as px
import plotly.graph_objects as go
import spacy
from better_profanity import profanity
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.tokenize import word_tokenize
from textblob import TextBlob
from wordcloud import WordCloud

try:
    from nltk.sentiment import SentimentIntensityAnalyzer  # VADER
except Exception:  # pragma: no cover
    SentimentIntensityAnalyzer = None  # type: ignore

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Check if spaCy's English model is installed, and download if necessary
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading spaCy model...")
    os.system("python -m spacy download en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


def analyze_sentiment(reviews):
    sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
    polarity_scores = []
    positive_reviews = []
    neutral_reviews = []
    negative_reviews = []

    for review in reviews:
        analysis = TextBlob(review)
        polarity_scores.append(analysis.sentiment.polarity)
        if analysis.sentiment.polarity > 0:
            sentiments['positive'] += 1
            positive_reviews.append(review)
        elif analysis.sentiment.polarity == 0:
            sentiments['neutral'] += 1
            neutral_reviews.append(review)
        else:
            sentiments['negative'] += 1
            negative_reviews.append(review)

    positive_keywords = extract_keywords(positive_reviews, 'positive')
    negative_keywords = extract_keywords(negative_reviews, 'negative')

    return (
        sentiments,
        positive_reviews,
        neutral_reviews,
        negative_reviews,
        polarity_scores,
        positive_keywords,
        negative_keywords,
    )


def analyze_sentiment_vader(reviews: List[str]):
    """Secondary sentiment engine using VADER for comparative analysis.

    Returns a dict of aggregate counts and detailed scores per review.
    If VADER is not available (dependency missing) falls back to zeros.
    """
    if not SentimentIntensityAnalyzer:
        return {"positive": 0, "neutral": 0, "negative": 0}, []
    sia = SentimentIntensityAnalyzer()
    scores: List[Dict[str, float]] = []
    agg = {"positive": 0, "neutral": 0, "negative": 0}
    for r in reviews:
        s = sia.polarity_scores(r)
        scores.append(s)
        compound = s['compound']
        if compound > 0.05:
            agg['positive'] += 1
        elif compound < -0.05:
            agg['negative'] += 1
        else:
            agg['neutral'] += 1
    return agg, scores

def extract_keywords(reviews, _sentiment):
    stop_words = set(stopwords.words('english'))
    words = []
    for review in reviews:
        tokens = word_tokenize(review.lower())
        words.extend([word for word in tokens if word.isalnum() and word not in stop_words])
    return Counter(words).most_common(10)

# Generate a word cloud from reviews
def generate_word_cloud(reviews):
    all_reviews = ' '.join(reviews)

    if all_reviews.strip():
        wordcloud = WordCloud(width=800, height=400).generate(all_reviews)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('static/wordcloud.png')


def create_visualizations(sentiments, polarity_scores, movie_details):
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [sentiments['positive'], sentiments['neutral'], sentiments['negative']]

    # Pie chart for sentiment distribution
    fig_pie = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=sizes,
                hoverinfo='label+percent',
                textinfo='percent',
            )
        ]
    )
    fig_pie.update_layout(title=f"Sentiment Analysis for {movie_details['title']}")

    # Bar chart for sentiment count
    fig_bar = go.Figure(
        data=[go.Bar(x=labels, y=sizes, marker={"color": ['green', 'gray', 'red']})]
    )
    fig_bar.update_layout(
        title=f"Sentiment Count for {movie_details['title']}",
        yaxis_title="Count",
    )

    # Histogram for polarity distribution
    # fig_hist = px.histogram(polarity_scores, nbins=20, labels={"value": "Polarity Score"})
    fig_hist = go.Figure(data=[go.Histogram(x=polarity_scores)])

    fig_hist.update_layout(
        title=f"Sentiment Polarity Distribution for {movie_details['title']}",
        xaxis_title="Polarity Score",
        yaxis_title="Frequency",
    )


    # Return the figures
    return fig_pie, fig_bar, fig_hist
stop_words = set(stopwords.words('english'))

# Custom list of inappropriate words (this is a sample, you can add more words)
inappropriate_words = {'fucking', 'ass', 'disgusting', 'shit', 'damn'}
def clean_review_text(reviews):
    cleaned_words = []
    for review in reviews:
        cleaned_review = profanity.censor(review)
        words = word_tokenize(cleaned_review.lower())
        doc = nlp(cleaned_review)
        important_entities = {ent.text.lower() for ent in doc.ents}

        for word in words:
            if _should_keep_word(word, important_entities):
                cleaned_words.append(word)

    return cleaned_words

def _should_keep_word(word: str, important_entities: set[str]) -> bool:
    """Decide whether a token is informative for word-frequency plots."""
    if not (word.isalpha() and len(word) > 2 and word not in stop_words):
        return False
    if word in important_entities:
        return True
    token = nlp(word)[0]
    return token.pos_ in ['NOUN', 'ADJ']

def plot_word_frequency(reviews, movie_details):
    # Clean and filter words
    words = clean_review_text(reviews)

    # Count word frequencies
    word_counts = FreqDist(words)

    # Get the 10 most common words
    most_common = word_counts.most_common(10)
    words, counts = zip(*most_common, strict=False)

    # Create a bar plot using Plotly
    fig = px.bar(
        x=words,
        y=counts,
        labels={'x': 'Words', 'y': 'Frequency'},
        title=f'Most Common Words in {movie_details["title"]} Reviews',
    )
    return fig


def plot_genre_distribution(genres):
    """
    Given a list of genres, generate a Plotly bar chart showing the distribution
    of movie genres.

    genres: str (comma-separated genres)

    Returns: Plotly figure in JSON format.
    """
    # Split the genres string into a list
    genre_list = genres.split(',')

    # Count the occurrences of each genre
    genre_count = Counter(genre_list)

    # Create a bar chart to visualize the genre distribution
    data = [
        go.Bar(
            x=list(genre_count.keys()),
            y=list(genre_count.values()),
            marker={"color": 'rgb(55, 83, 109)'}  # Optional styling for bars
        )
    ]

    layout = go.Layout(
        title="Genre Distribution",
        xaxis={"title": "Genres"},
        yaxis={"title": "Frequency"},
        showlegend=False,
    )

    fig = go.Figure(data=data, layout=layout)

    # Return Plotly figure as JSON
    return fig
