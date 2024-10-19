from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Analyze sentiment of the reviews using TextBlob and return detailed lists
def analyze_sentiment(reviews):
    sentiments = {'positive': 0, 'neutral': 0, 'negative': 0}
    positive_reviews = []
    neutral_reviews = []
    negative_reviews = []
    
    for review in reviews:
        analysis = TextBlob(review)
        if analysis.sentiment.polarity > 0:
            sentiments['positive'] += 1
            positive_reviews.append(review)
        elif analysis.sentiment.polarity == 0:
            sentiments['neutral'] += 1
            neutral_reviews.append(review)
        else:
            sentiments['negative'] += 1
            negative_reviews.append(review)
    
    return sentiments, positive_reviews, neutral_reviews, negative_reviews

# Generate a word cloud from reviews
def generate_word_cloud(reviews):
    all_reviews = ' '.join(reviews)
    
    if all_reviews.strip():
        wordcloud = WordCloud(width=800, height=400).generate(all_reviews)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('static/wordcloud.png')

# Create sentiment visualizations
def create_visualizations(sentiments, movie_details):
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [sentiments['positive'], sentiments['neutral'], sentiments['negative']]
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(f"Sentiment Analysis for {movie_details['title']}")
    plt.savefig('static/sentiment_pie.png')
