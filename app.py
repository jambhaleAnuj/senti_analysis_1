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
            sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores = analyze_sentiment(reviews)
            generate_word_cloud(reviews)
            create_visualizations(sentiments, polarity_scores, movie_details)
            
            # Pass the sentiment data and categorized reviews to the results page
            return redirect(url_for('results', 
                                    movie=movie_details['title'],
                                    year=movie_details['year'],
                                    rating=movie_details['rating'],
                                    genres=movie_details['genres'],
                                    plot = movie_details['plot'],
                                    actors =  movie_details['actor'],
                                    poster=movie_details['poster'],  # Add poster
                                    language = movie_details['language'],
                                    country = movie_details['country'],
                                    writer = movie_details['writer'],
                                    awards = movie_details['awards'],
                                    director = movie_details['director'],
                                    box_office=movie_details['box_office'],
                                    release_date=movie_details['release_date'],
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
    positive = request.args.get('positive')
    neutral = request.args.get('neutral')
    negative = request.args.get('negative')
    total = request.args.get('total')
    actors = request.args.get('actors')

    return render_template('results.html', 
                           movie=movie, 
                           plot = plot,
                           actors = actors,
                           director = director,
                           poster = poster,
                           language = language,
                           country = country,
                           writer = writer,
                           awards= awards,
                           year=year,
                           rating=rating,
                           genres=genres,
                           box_office=box_office,
                           release_date=release_date,
                           positive=positive, 
                           neutral=neutral, 
                           negative=negative, 
                           total=total)

if __name__ == '__main__':
    app.run(debug=True)
