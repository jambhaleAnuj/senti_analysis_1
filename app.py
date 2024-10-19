from flask import Flask, render_template, request, redirect, url_for
from imdb_scraper import fetch_imdb_reviews
from sentiment_analysis import analyze_sentiment, generate_word_cloud, create_visualizations

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        imdb_url = request.form['imdb_url']
        reviews, movie_details = fetch_imdb_reviews(imdb_url)
        
        if reviews:
            sentiments, positive_reviews, neutral_reviews, negative_reviews = analyze_sentiment(reviews)
            generate_word_cloud(reviews)
            create_visualizations(sentiments, movie_details)
            
            # Pass the sentiment data and categorized reviews to the results page
            return redirect(url_for('results', 
                                    movie=movie_details['title'],
                                    positive=len(positive_reviews),
                                    neutral=len(neutral_reviews),
                                    negative=len(negative_reviews),
                                    total=len(reviews)
                                   ))
        else:
            return render_template('index.html', error="No reviews found for this IMDb URL.")
    
    return render_template('index.html')

@app.route('/results')
def results():
    movie = request.args.get('movie')
    positive = request.args.get('positive')
    neutral = request.args.get('neutral')
    negative = request.args.get('negative')
    total = request.args.get('total')

    return render_template('results.html', movie=movie, positive=positive, neutral=neutral, negative=negative, total=total)

if __name__ == '__main__':
    app.run(debug=True)
