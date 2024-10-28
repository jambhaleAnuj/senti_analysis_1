from textblob import TextBlob
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import matplotlib
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

# Create sentiment visualizations
def create_visualizations(sentiments, polarity_scores, movie_details):
    labels = ['Positive', 'Neutral', 'Negative']
    sizes = [sentiments['positive'], sentiments['neutral'], sentiments['negative']]
    
    # Pie chart for sentiment distribution
    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(f"Sentiment Analysis for {movie_details['title']}")
    plt.savefig('static/sentiment_pie.png')

    # Bar chart for sentiment count
    plt.figure(figsize=(8, 6))
    sns.barplot(x=labels, y=sizes, palette='coolwarm')
    plt.title(f"Sentiment Count for {movie_details['title']}")
    plt.ylabel("Count")
    plt.savefig('static/sentiment_bar.png')

    # Histogram for polarity distribution
    plt.figure(figsize=(8, 6))
    plt.hist(polarity_scores, bins=20, color='skyblue', edgecolor='black')
    plt.title(f"Sentiment Polarity Distribution for {movie_details['title']}")
    plt.xlabel("Polarity Score")
    plt.ylabel("Frequency")
    plt.savefig('static/sentiment_histogram.png')