import json
from plotly.utils import PlotlyJSONEncoder
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
from flask import Flask, render_template, request, redirect, url_for
from imdb_scraper import fetch_movie_reviews_and_details, fetch_trending_movies
from sentiment_analysis import analyze_sentiment, generate_word_cloud, create_visualizations,plot_word_frequency,plot_genre_distribution
import json
from flask import jsonify
from youtube_scraper import search_trailer_video_id, get_trailer_comments

import requests

app = Flask(__name__)

# FALLBACK_TRENDING = [
#     {
#         'title': 'Oppenheimer',
#         'link': 'oppenheimer',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/7/8/4/3/2/8/784328-oppenheimer-0-1000-0-1500-crop.jpg?v=e3c6e7a32c'
#     },
#     {
#         'title': 'Barbie',
#         'link': 'barbie',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/2/7/7/0/6/4/277064-barbie-0-230-0-345-crop.jpg?v=1b83dc7a71'
#     },
#     {
#         'title': 'Fight Club',
#         'link': 'fight-club',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/5/1/5/6/8/51568-fight-club-0-1000-0-1500-crop.jpg?v=768b32dfa4'
#     },
#     {
#         'title': 'Parasite',
#         'link': 'parasite',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/4/2/6/4/0/6/426406-parasite-0-1000-0-1500-crop.jpg?v=8f5653f710'
#     },
#     {
#         'title': 'Everything Everywhere All at Once',
#         'link': 'everything-everywhere-all-at-once',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/4/7/4/4/7/4/474474-everything-everywhere-all-at-once-0-1000-0-1500-crop.jpg?v=281f1a041e'
#     },
#     {
#         'title': 'La La Land',
#         'link': 'la-la-land',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/2/4/0/3/4/4/240344-la-la-land-0-1000-0-1500-crop.jpg?v=053670ff84'
#     },
#     {
#         'title': 'Joker',
#         'link': 'joker',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/4/0/6/7/7/5/406775-joker-0-1000-0-1500-crop.jpg?v=e4ea7f98cc '
#     },
#     {
#         'title': 'Whiplash',
#         'link': 'whiplash',
#         'image': 'https://a.ltrbxd.com/resized/sm/upload/cl/dn/kr/f1/4C9LHDxMsoYI0S3iMPZdm3Oevwo-0-1000-0-1500-crop.jpg?v=d13ea36528'
#     },
#     {
#         'title': 'Inception',
#         'link': 'inception',
#         'image': 'https://a.ltrbxd.com/resized/sm/upload/sv/95/s9/4j/inception-0-1000-0-1500-crop.jpg?v=30d7224316'
#     },
#     {
#         'title': 'Spider-Man: Into the Spider-Verse',
#         'link': 'spider-man-into-the-spider-verse',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/2/5/1/9/4/3/251943-spider-man-into-the-spider-verse-0-1000-0-1500-crop.jpg?v=538fe0ada6'
#     },
#     {
#         'title': 'The Batman',
#         'link': 'the-Batman',
#         'image': 'https://a.ltrbxd.com/resized/film-poster/3/4/8/9/1/4/348914-the-batman-0-1000-0-1500-crop.jpg?v=ec12a8b7ce'
#     },
#     {
#         'title': 'The Shawshank Redemption',
#         'link': 'the-shawshank-redemption',
#         'image': 'https://a.ltrbxd.com/resized/sm/upload/7l/hn/46/uz/zGINvGjdlO6TJRu9wESQvWlOKVT-0-1000-0-1500-crop.jpg?v=8736d1c395'
#     },
#     # Add more fallback movies as needed
# ]


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

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     trending_movies = fetch_trending_movies()
#     print(trending_movies)

  
        
#     if not trending_movies:
#         print("Both methods failed, using fallback data")
#         trending_movies = FALLBACK_TRENDING

#     if request.method == 'POST':
#         movie_title = request.form['letterboxd_url']
#         letterboxd_url = request.form['letterboxd_url']
#         letterboxd_url = letterboxd_url.replace(' ', '-').lower()

#         letterboxd_urls = 'https://letterboxd.com/film/'+letterboxd_url
        
#         reviews, movie_details,similar_movies = fetch_movie_reviews_and_details(movie_title, letterboxd_urls)
        
#         print(similar_movies)
#         if reviews:
#             sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords = analyze_sentiment(reviews)
#             generate_word_cloud(reviews)
#             create_visualizations(sentiments, polarity_scores, movie_details)
           
            
#             positive_keywords_json = json.dumps(dict(positive_keywords))
#             negative_keywords_json = json.dumps(dict(negative_keywords))
#             reviews_json = json.dumps(reviews)
#             return redirect(url_for('results', 
#                                     movie=movie_details['title'],
#                                     year=movie_details['year'],
#                                     rating=movie_details['rating'],
#                                     genres=movie_details['genres'],
#                                     plot=movie_details['plot'],
#                                     actors=movie_details['actor'],
#                                     poster=movie_details['poster'],
#                                     language=movie_details['language'],
#                                     country=movie_details['country'],
#                                     writer=movie_details['writer'],
#                                     awards=movie_details['awards'],
#                                     director=movie_details['director'],
#                                     box_office=movie_details['box_office'],
#                                     release_date=movie_details['release_date'],
#                                     positive=len(positive_reviews),
#                                     neutral=len(neutral_reviews),
#                                     negative=len(negative_reviews),
#                                     total=len(reviews),
#                                     rev = reviews_json,
#                                     positive_keywords=positive_keywords_json,
#                                     negative_keywords=negative_keywords_json,
#                                     similar_movies=json.dumps(similar_movies)

#                                    ))
#         else:
#             return render_template('index.html', error="No reviews found for this movie.", trending_movies=trending_movies)
    
    
#     else:
#         # Handle the case when coming from a similar movie link
#         letterboxd_url = request.args.get('letterboxd_url')
#         if letterboxd_url:
#             letterboxd_url = letterboxd_url.replace(' ', '-').lower()
#             letterboxd_urls = 'https://letterboxd.com/film/' + letterboxd_url
            
#             reviews, movie_details, similar_movies = fetch_movie_reviews_and_details(letterboxd_url, letterboxd_urls)
            
    
#     return render_template('index.html', trending_movies=trending_movies)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     trending_movies = fetch_trending_movies()
#     print(trending_movies)

#     if not trending_movies:
#         print("Both methods failed, using fallback data")
#         trending_movies = FALLBACK_TRENDING

#     if request.method == 'POST':
#         # For movie search via letterboxd URL
#         movie_title = request.form['letterboxd_url']
#         letterboxd_url = request.form['letterboxd_url']
#         letterboxd_url = letterboxd_url.replace(' ', '-').lower()
#         letterboxd_urls = 'https://letterboxd.com/film/' + letterboxd_url
        
#         reviews, movie_details, similar_movies = fetch_movie_reviews_and_details(movie_title, letterboxd_urls)

#         print(similar_movies)
#         if reviews:
#             sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords = analyze_sentiment(reviews)
#             generate_word_cloud(reviews)
#             create_visualizations(sentiments, polarity_scores, movie_details)

#             positive_keywords_json = json.dumps(dict(positive_keywords))
#             negative_keywords_json = json.dumps(dict(negative_keywords))
#             reviews_json = json.dumps(reviews)

#             return redirect(url_for('results', 
#                                     movie=movie_details['title'],
#                                     year=movie_details['year'],
#                                     rating=movie_details['rating'],
#                                     genres=movie_details['genres'],
#                                     plot=movie_details['plot'],
#                                     actors=movie_details['actor'],
#                                     poster=movie_details['poster'],
#                                     language=movie_details['language'],
#                                     country=movie_details['country'],
#                                     writer=movie_details['writer'],
#                                     awards=movie_details['awards'],
#                                     director=movie_details['director'],
#                                     box_office=movie_details['box_office'],
#                                     release_date=movie_details['release_date'],
#                                     positive=len(positive_reviews),
#                                     neutral=len(neutral_reviews),
#                                     negative=len(negative_reviews),
#                                     total=len(reviews),
#                                     rev=reviews_json,
#                                     positive_keywords=positive_keywords_json,
#                                     negative_keywords=negative_keywords_json,
#                                     similar_movies=json.dumps(similar_movies)
#                                    ))
#         else:
#             return render_template('index.html', error="No reviews found for this movie.", trending_movies=trending_movies)

#     else:
#         # Handle the case when coming from a similar movie link (GET request)
#         letterboxd_url = request.args.get('letterboxd_url')
#         if letterboxd_url:
#             letterboxd_url = letterboxd_url.replace(' ', '-').lower()
#             letterboxd_urls = 'https://letterboxd.com/film/' + letterboxd_url
            
#             reviews, movie_details, similar_movies = fetch_movie_reviews_and_details(letterboxd_url, letterboxd_urls)

#             if reviews:
#                 sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords = analyze_sentiment(reviews)
#                 generate_word_cloud(reviews)
#                 create_visualizations(sentiments, polarity_scores, movie_details)

#                 positive_keywords_json = json.dumps(dict(positive_keywords))
#                 negative_keywords_json = json.dumps(dict(negative_keywords))
#                 reviews_json = json.dumps(reviews)

#                 return redirect(url_for('results', 
#                                         movie=movie_details['title'],
#                                         year=movie_details['year'],
#                                         rating=movie_details['rating'],
#                                         genres=movie_details['genres'],
#                                         plot=movie_details['plot'],
#                                         actors=movie_details['actor'],
#                                         poster=movie_details['poster'],
#                                         language=movie_details['language'],
#                                         country=movie_details['country'],
#                                         writer=movie_details['writer'],
#                                         awards=movie_details['awards'],
#                                         director=movie_details['director'],
#                                         box_office=movie_details['box_office'],
#                                         release_date=movie_details['release_date'],
#                                         positive=len(positive_reviews),
#                                         neutral=len(neutral_reviews),
#                                         negative=len(negative_reviews),
#                                         total=len(reviews),
#                                         rev=reviews_json,
#                                         positive_keywords=positive_keywords_json,
#                                         negative_keywords=negative_keywords_json,
#                                         similar_movies=json.dumps(similar_movies)
#                                        ))
#             else:
#                 return render_template('index.html', error="No reviews found for this movie.", trending_movies=trending_movies)
        
#     return render_template('index.html', trending_movies=trending_movies)


# @app.route('/', methods=['GET', 'POST'])
# def index():
#     # Fetch the trending movies
#     trending_movies = fetch_trending_movies()

#     if not trending_movies:
#         trending_movies = FALLBACK_TRENDING

#     if request.method == 'POST':
#         # Handle search request from the form
#         movie_title = request.form['letterboxd_url']
#         letterboxd_url = movie_title.replace(' ', '-').lower()

#         # Construct the full URL for the movie (search case)
#         letterboxd_full_url = f'https://letterboxd.com/film/{letterboxd_url}/'

#         # Fetch reviews and details for the searched movie
#         reviews, movie_details, similar_movies = fetch_movie_reviews_and_details(movie_title, letterboxd_full_url)

#         # Ensure each similar movie has the full URL
#         for movie in similar_movies:
#             movie['url'] = f'https://letterboxd.com/film/{letterboxd_url}/'

#         if reviews:
#             sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords = analyze_sentiment(reviews)
#             generate_word_cloud(reviews)
#             create_visualizations(sentiments, polarity_scores, movie_details)
            
#             positive_keywords_json = json.dumps(dict(positive_keywords))
#             negative_keywords_json = json.dumps(dict(negative_keywords))
#             reviews_json = json.dumps(reviews)
            
#             # Redirect to the results page
#             return redirect(url_for('results', 
#                                     movie=movie_details['title'],
#                                     year=movie_details['year'],
#                                     rating=movie_details['rating'],
#                                     genres=movie_details['genres'],
#                                     plot=movie_details['plot'],
#                                     actors=movie_details['actor'],
#                                     poster=movie_details['poster'],
#                                     language=movie_details['language'],
#                                     country=movie_details['country'],
#                                     writer=movie_details['writer'],
#                                     awards=movie_details['awards'],
#                                     director=movie_details['director'],
#                                     box_office=movie_details['box_office'],
#                                     release_date=movie_details['release_date'],
#                                     positive=len(positive_reviews),
#                                     neutral=len(neutral_reviews),
#                                     negative=len(negative_reviews),
#                                     total=len(reviews),
#                                     rev=reviews_json,
#                                     positive_keywords=positive_keywords_json,
#                                     negative_keywords=negative_keywords_json,
#                                     similar_movies=json.dumps(similar_movies)
#                                    ))
#         else:
#             # In case no reviews are found, show an error on the homepage
#             return render_template('index.html', error="No reviews found for this movie.", trending_movies=trending_movies)

#     else:
#         # Handle the case when coming from a similar movie link
#         letterboxd_url = request.args.get('letterboxd_url')
#         if letterboxd_url:
#             letterboxd_url = letterboxd_url.replace(' ', '-').lower()
            
#             # Construct the full URL for the similar movie
#             letterboxd_full_url = f'https://letterboxd.com/film/{letterboxd_url}/'
            
#             # Fetch reviews and details for the selected similar movie
#             reviews, movie_details, similar_movies = fetch_movie_reviews_and_details(letterboxd_url, letterboxd_full_url)


#             print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> \n "+letterboxd_full_url +"\n"+movie_details)
#             # Ensure each similar movie has the full URL
#             for movie in similar_movies:
#                 movie['url'] = f'https://letterboxd.com/film/{movie["link"]}/'

#             if reviews:
#                 sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords = analyze_sentiment(reviews)
#                 generate_word_cloud(reviews)
#                 create_visualizations(sentiments, polarity_scores, movie_details)
                
#                 positive_keywords_json = json.dumps(dict(positive_keywords))
#                 negative_keywords_json = json.dumps(dict(negative_keywords))
#                 reviews_json = json.dumps(reviews)
                
#                 return redirect(url_for('results', 
#                                         movie=movie_details['title'],
#                                         year=movie_details['year'],
#                                         rating=movie_details['rating'],
#                                         genres=movie_details['genres'],
#                                         plot=movie_details['plot'],
#                                         actors=movie_details['actor'],
#                                         poster=movie_details['poster'],
#                                         language=movie_details['language'],
#                                         country=movie_details['country'],
#                                         writer=movie_details['writer'],
#                                         awards=movie_details['awards'],
#                                         director=movie_details['director'],
#                                         box_office=movie_details['box_office'],
#                                         release_date=movie_details['release_date'],
#                                         positive=len(positive_reviews),
#                                         neutral=len(neutral_reviews),
#                                         negative=len(negative_reviews),
#                                         total=len(reviews),
#                                         rev=reviews_json,
#                                         positive_keywords=positive_keywords_json,
#                                         negative_keywords=negative_keywords_json,
#                                         similar_movies=json.dumps(similar_movies)
#                                        ))
#             else:
#                 # If no reviews for the similar movie, render error
#                 return render_template('index.html', error="No reviews found for this movie.", trending_movies=trending_movies)

#     # Render the homepage with trending movies (if no POST request)
#     return render_template('index.html', trending_movies=trending_movies)


@app.route('/', methods=['GET', 'POST'])
def index():
    # Fetch the trending movies
    trending_movies = fetch_trending_movies()

    
    #################################### UN-COMMENT THIS TO GET THE REALTIME TRENDING MOVIES #############################################
    # if not trending_movies:
    #     trending_movies = FALLBACK_TRENDING

    if  trending_movies:
        trending_movies = FALLBACK_TRENDING


    if request.method == 'POST':
        # Get movie name or similar movie name from form
        movie_name = request.form.get('letterboxd_url')  # Movie name input from the form

        # If it's a search or similar movie click
        if movie_name:  # Either a search or a click on similar movie


            print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n"+ movie_name)
            # Format the movie title for the URL (make lowercase and replace spaces with dashes)
            letterboxd_url = movie_name.replace(' ', '-').lower()
            letterboxd_full_url = f'https://letterboxd.com/film/{letterboxd_url}/'

            # Fetch reviews and details for the movie (either from search or from similar movie click)
            reviews, movie_details, similar_movies = fetch_movie_reviews_and_details(movie_name, letterboxd_full_url)

            # Ensure each similar movie has the correct URL
            # for movie in similar_movies:
            #     movie['url'] = f'https://letterboxd.com/film/{movie["link"]}/'

            if reviews:
                # Perform sentiment analysis
                sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords = analyze_sentiment(reviews)
                generate_word_cloud(reviews)
                create_visualizations(sentiments, polarity_scores, movie_details)
                
                # Convert keywords to JSON
                positive_keywords_json = json.dumps(dict(positive_keywords))
                negative_keywords_json = json.dumps(dict(negative_keywords))
                reviews_json = json.dumps(reviews)
                
                # Redirect to the results page with movie data and sentiment analysis results
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
                                        # positive_reviews = positive_reviews,
                                        neutral=len(neutral_reviews),
                                        negative=len(negative_reviews),
                                        total=len(reviews),
                                        rev=reviews_json,
                                        positive_keywords=positive_keywords_json,
                                        negative_keywords=negative_keywords_json,
                                        similar_movies=json.dumps(similar_movies)
                                       ))
            else:
                # In case no reviews are found for the movie
                return render_template('index.html', error="No reviews found for this movie.", trending_movies=trending_movies)

    else:
        # Handle the case for initial page load (GET request)
        letterboxd_url = request.args.get('letterboxd_url')
        if letterboxd_url:
            # Handle the URL of a similar movie
            letterboxd_url = letterboxd_url.replace(' ', '-').lower()
            letterboxd_full_url = f'https://letterboxd.com/film/{letterboxd_url}/'
            
            # Fetch reviews and details for the selected similar movie
            reviews, movie_details, similar_movies = fetch_movie_reviews_and_details(letterboxd_url, letterboxd_full_url)

            # Ensure each similar movie has the full URL
            for movie in similar_movies:
                movie['url'] = f'https://letterboxd.com/film/{movie["link"]}/'

            if reviews:
                # Sentiment analysis and word cloud generation
                sentiments, positive_reviews, neutral_reviews, negative_reviews, polarity_scores, positive_keywords, negative_keywords = analyze_sentiment(reviews)
                generate_word_cloud(reviews)
                create_visualizations(sentiments, polarity_scores, movie_details)
                
                # Convert keywords to JSON
                positive_keywords_json = json.dumps(dict(positive_keywords))
                negative_keywords_json = json.dumps(dict(negative_keywords))
                reviews_json = json.dumps(reviews)
                
                # Redirect to the results page
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
                                        rev=reviews_json,
                                        # positive_reviews = positive_reviews,
                                        positive_keywords=positive_keywords_json,
                                        negative_keywords=negative_keywords_json,
                                        similar_movies=json.dumps(similar_movies)
                                       ))
            else:
                # If no reviews for the similar movie, show an error
                return render_template('index.html', error="No reviews found for this movie.", trending_movies=trending_movies)

    # Render the homepage with trending movies (if no POST request)
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

        similar_movies = json.loads(request.args.get('similar_movies'))

         # Generate word frequency plot
        # reviews = request.args.get('rev').split(';')  # You should pass the reviews as a string
        reviews = json.loads(request.args.get('rev'))
        sentiment = request.args.get('sentiment')  # Pass the sentiment (positive, negative, etc.)

        print(".....")
        print(genres)


########################################### FOR YOUTUBE ###############################################

  # 1. YouTube Trailer Comments
        print("ENTERED YOUTUBE")
        trailer_comments = get_trailer_comments(movie)
        # Make sure each comment is being passed as a string
        # print("YOUTUBE TRAILER COMMENTS: \n",[comment['text'] for comment in trailer_comments])

        # 2. Sentiment analysis of YouTube comments
        if trailer_comments:
            yt_sentiments, yt_positive, yt_neutral, yt_negative, yt_polarity_scores, yt_positive_keywords, yt_negative_keywords = analyze_sentiment([comment['text'] for comment in trailer_comments])
        else:
            yt_sentiments = yt_positive = yt_neutral = yt_negative = yt_polarity_scores = yt_positive_keywords = yt_negative_keywords = []

        print("YOUTUBE POSITIVE",yt_sentiments)
        print(yt_sentiments['positive'])
        print(yt_negative)
        print(yt_neutral)
        # 3. Generate visualizations for trailer comments (pie chart, bar chart)
        # Pie chart for sentiment distribution

        sentiment_counts = {'positive': yt_sentiments['positive'], 'neutral': yt_sentiments['neutral'], 'negative': yt_sentiments['negative']}
        yt_labels = ['Positive', 'Neutral', 'Negative']
        sizes = [yt_sentiments['positive'], yt_sentiments['neutral'], yt_sentiments['negative']]

        # fig_pie_yt = px.pie(names=list(sentiment_counts.keys()), values=list(sentiment_counts.values()), title=f"Sentiment Distribution for Trailer Comments of {movie}")
        # fig_pie_yt = go.Figure()
        fig_pie_yt = go.Figure(data=[go.Pie(labels=yt_labels, values=sizes, hoverinfo='label+percent', textinfo='percent')])

        pie_json_yt = json.dumps(fig_pie_yt, cls=PlotlyJSONEncoder)

        # Bar chart for polarity scores
        # fig_bar_yt = px.bar(x=['positive', 'neutral', 'negative'], y=[len(yt_positive), len(yt_neutral), len(yt_negative)], title=f"Sentiment Breakdown for Trailer Comments of {movie}")
        
        fig_bar_yt = go.Figure(data=[go.Bar(x=yt_labels, y=sizes, marker=dict(color=['green', 'gray', 'red']))])
        
        bar_json_yt = json.dumps(fig_bar_yt, cls=PlotlyJSONEncoder)

        # Generate word frequency plot for YouTube comments
        word_freq_yt = plot_word_frequency([comment['text'] for comment in trailer_comments], sentiment, {'title': movie})
        word_freq_json_yt = json.dumps(word_freq_yt, cls=PlotlyJSONEncoder)


########################################################################################################
        #Genre Distribution
        plt_genre = plot_genre_distribution(genres)
        # print(plt_genre)

        genre_fig = plot_genre_distribution(genres)
    
    # Convert the Plotly figure to JSON to pass to the frontend
        genre_plot_json = json.dumps(genre_fig, cls=PlotlyJSONEncoder)


        # Create the word frequency plot
        word_freq_plot_html = plot_word_frequency(reviews, sentiment,{'title':movie})
        word_freq_plot_json = json.dumps(word_freq_plot_html,cls=PlotlyJSONEncoder)

        print("POSITIVE",positive)
        # Get visualizations
        fig_pie, fig_bar, fig_hist = create_visualizations(
            {'positive': positive, 'neutral': neutral, 'negative': negative}, 
            [positive, neutral, negative],  # Example polarity scores
            {'title': movie}
        )
        
        pie_json = json.dumps(fig_pie, cls=PlotlyJSONEncoder)
        bar_json = json.dumps(fig_bar, cls=PlotlyJSONEncoder)
        hist_json = json.dumps(fig_hist, cls=PlotlyJSONEncoder)
        
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
                               negative_keywords=negative_keywords,
                               similar_movies=similar_movies,
                               pie_chart=pie_json,
                               bar_chart=bar_json,
                               hist_chart=hist_json,
                               word_freq_plot=word_freq_plot_json,
                               genre_plot_json=genre_plot_json,
                                pie_chart_yt=pie_json_yt,
                               bar_chart_yt=bar_json_yt,
                               word_freq_plot_yt=word_freq_json_yt)

    except Exception as e:
        print(f"Error in results route: {str(e)}")
        return render_template('error.html', error=str(e))



OMDB_API_KEY = '36650a58'


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
    app.run(debug=True)
