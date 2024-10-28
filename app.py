from flask import Flask, render_template, request, redirect, url_for
from imdb_scraper import fetch_movie_reviews_and_details, fetch_trending_movies
from sentiment_analysis import analyze_sentiment, generate_word_cloud, create_visualizations
import json

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    trending_movies = fetch_trending_movies()
    print(trending_movies)
    if request.method == 'POST':
        movie_title = request.form['letterboxd_url']
        letterboxd_url = request.form['letterboxd_url']
        letterboxd_url = letterboxd_url.replace(' ', '-').lower()

        letterboxd_urls = 'https://letterboxd.com/film/'+letterboxd_url
        
        reviews, movie_details = fetch_movie_reviews_and_details(movie_title, letterboxd_urls)
        
        if reviews:
            sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords = analyze_sentiment(reviews)
            generate_word_cloud(reviews)
            create_visualizations(sentiments, polarity_scores, movie_details)
            
            positive_keywords_json = json.dumps(dict(positive_keywords))
            negative_keywords_json = json.dumps(dict(negative_keywords))
            
            return redirect(url_for('results', 
                                    movie=movie_details['title'],
                                    year=movie_details['year'],
                                    rating=movie_details['rating'],
                                    genres=movie_details['genres'],
                                    plot=movie_details['plot'],
                                    actors=movie_details['actor'],
                                    poster=movie_details['poster'],
                                    language=movie_details['language'],
                                    country=movie_details['country'],
                                    writer=movie_details['writer'],
                                    awards=movie_details['awards'],
                                    director=movie_details['director'],
                                    box_office=movie_details['box_office'],
                                    release_date=movie_details['release_date'],
                                    positive=len(positive_reviews),
                                    neutral=len(neutral_reviews),
                                    negative=len(negative_reviews),
                                    total=len(reviews),
                                    positive_keywords=positive_keywords_json,
                                    negative_keywords=negative_keywords_json
                                   ))
        else:
            return render_template('index.html', error="No reviews found for this movie.", trending_movies=trending_movies)
    
    return render_template('index.html', trending_movies=trending_movies)

@app.route('/results')
def results():
    try:
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
        positive = int(request.args.get('positive'))
        neutral = int(request.args.get('neutral'))
        negative = int(request.args.get('negative'))
        total = int(request.args.get('total'))
        actors = request.args.get('actors')
        
        positive_keywords = json.loads(request.args.get('positive_keywords'))
        negative_keywords = json.loads(request.args.get('negative_keywords'))
        
        positive_keywords = [(word, count) for word, count in positive_keywords.items()]
        negative_keywords = [(word, count) for word, count in negative_keywords.items()]

        return render_template('results.html', 
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
                               positive_keywords=positive_keywords,
                               negative_keywords=negative_keywords)
    except Exception as e:
        print(f"Error in results route: {str(e)}")
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)