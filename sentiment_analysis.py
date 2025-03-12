
from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import matplotlib
import plotly.graph_objects as go
import plotly.express as px
matplotlib.use('Agg')

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

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
    
    print("positive reviews:",positive_reviews)
    print("...........")
    print("Negative Reviews: ",negative_reviews)
    return sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords

def extract_keywords(reviews, sentiment):
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
    fig_pie = go.Figure(data=[go.Pie(labels=labels, values=sizes, hoverinfo='label+percent', textinfo='percent')])
    fig_pie.update_layout(title=f"Sentiment Analysis for {movie_details['title']}")

    # Bar chart for sentiment count
    fig_bar = go.Figure(data=[go.Bar(x=labels, y=sizes, marker=dict(color=['green', 'gray', 'red']))])
    fig_bar.update_layout(title=f"Sentiment Count for {movie_details['title']}", yaxis_title="Count")

    # Histogram for polarity distribution
    # fig_hist = px.histogram(polarity_scores, nbins=20, labels={"value": "Polarity Score"})
    fig_hist = go.Figure(data=[go.Histogram(x=polarity_scores)])

    fig_hist.update_layout(title=f"Sentiment Polarity Distribution for {movie_details['title']}", xaxis_title="Polarity Score", yaxis_title="Frequency")

    
    # Return the figures
    return fig_pie, fig_bar, fig_hist


def plot_word_frequency(reviews, sentiment):
    words = []
    for review in reviews:
        words.extend(review.split())
    
    word_counts = Counter(words)
    most_common = word_counts.most_common(10)  # Get the 10 most common words
    words, counts = zip(*most_common)
    
    fig = px.bar(x=words, y=counts, labels={'x': 'Words', 'y': 'Frequency'}, title=f'Most Common Words in {sentiment} Reviews')
    return fig