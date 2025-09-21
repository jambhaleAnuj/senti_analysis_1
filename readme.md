<div align="center">

# 🎬 Movie Review Sentiment Analysis Platform

Educational & developer-friendly Flask + NLP app that aggregates movie reviews from **Letterboxd**, **Rotten Tomatoes**, **OMDb**, and **YouTube trailer comments** to perform sentiment analysis, keyword extraction, genre visualization, and interactive Plotly dashboards.

[![CI](https://github.com/jambhaleAnuj/senti_analysis_1/actions/workflows/ci.yml/badge.svg)](../../actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Status](https://img.shields.io/badge/Project-Educational-informational)
[![Contributions Welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

</div>

## 📌 Overview

This project was originally built for a college assignment and has been upgraded to a structured, extensible, and production-style educational repository. It demonstrates:

-   Web scraping (ethical & rate-conscious patterns) for movie reviews
-   Sentiment analysis using **TextBlob**, **NLTK**, optional profanity filtering, and basic keyword extraction
-   Visualization with **Plotly** (distribution, polarity, keywords, genre breakdown)
-   Comparison of audience mood **before release (YouTube trailer comments)** vs **after release (user reviews)**
-   Clean project structure, Docker build, CI pipeline, tests, and contribution standards

> ⚠️ Disclaimer: This repository is for learning & research. Always review platform Terms of Service before scraping and avoid abusive traffic patterns.

## 🚀 Features

-   🔍 Enter a movie title – automatic metadata & poster retrieval via OMDb
-   🗂 Aggregated reviews (Letterboxd + Rotten Tomatoes users)
-   ▶️ Pre-release sentiment via YouTube trailer comments
-   📊 Interactive charts: pie, bar, polarity histogram, genre distribution
-   🧠 Keyword extraction for positive & negative reviews
-   ☁️ Word cloud generation
-   🧼 Profanity filtering & basic NLP cleanup (spaCy + NLTK)
-   🐳 Dockerized for reproducibility
-   ✅ CI: linting, tests, security scanning

## 📊 Sample Screens

![Home](/screenshots/HomeScreen.png)
![Results 1](/screenshots/ResultScreen1.png)
![Results 2](/screenshots/ResultScreen2.png)
![Results 3](/screenshots/ResultScreen3.png)  
![Results 4](/screenshots/ResultScreen4.png)

## 🧱 Architecture

| Component               | Purpose                                                                 |
| ----------------------- | ----------------------------------------------------------------------- |
| `app.py`                | Flask web server, routing & orchestration                               |
| `imdb_scraper.py`       | Fetches metadata (OMDb) + Letterboxd + Rotten Tomatoes + similar movies |
| `youtube_scraper.py`    | Trailer search + comment harvesting (YouTube Data API)                  |
| `sentiment_analysis.py` | Sentiment classification, keyword extraction, word cloud, plots         |
| `templates/`            | Jinja2 HTML templates for UI                                            |
| `static/`               | CSS & generated plot assets                                             |
| `config.py`             | Central environment & app configuration                                 |
| `tests/`                | Pytest-based unit tests                                                 |

## 🛠 Tech Stack

-   Python 3.11
-   Flask, Plotly, TextBlob, NLTK, spaCy, WordCloud
-   BeautifulSoup4, Requests
-   Google API Client (YouTube Data API)
-   Docker, GitHub Actions, Ruff, Black, Pytest

## 📦 Quick Start

### 1. Clone & Prepare

```bash
git clone https://github.com/jambhaleAnuj/senti_analysis_1.git
cd senti_analysis_1
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
pip install -r requirements-dev.txt  # optional for contributors
```

### 2. Configure Environment

Copy `.env.example` → `.env` and fill in:

```ini
OMDB_API_KEY=your_key
YOUTUBE_API=your_key
GEMMA_API_KEY = your_key
```

### 3. Run

```bash
python app.py
```

Open: <http://127.0.0.1:5000>

### 4. Docker (Optional)

```bash
docker build -t movie-sentiment .
docker run --rm -p 5000:5000 --env-file .env movie-sentiment
```

## 🧪 Testing

```bash
pytest -q
```

## 🧹 Code Quality

```bash
ruff check .
black .
```

## 🌐 SEO & Discoverability

Relevant keywords included: Movie Sentiment Analysis, Flask NLP, YouTube Comments Sentiment, Rotten Tomatoes reviews, Letterboxd scraping, Plotly dashboard, TextBlob sentiment, Python movie analytics, genre visualization, pre-release vs post-release audience mood.

## 🔐 Environment Variables

| Variable        | Purpose                    | Required                               |
| --------------- | -------------------------- | -------------------------------------- |
| `OMDB_API_KEY`  | Movie metadata & posters   | Yes (fallback demo key used if absent) |
| `YOUTUBE_API`   | Trailer comments sentiment | Optional (feature disabled if missing) |
| `GEMMA_API_KEY` | Trailer comments sentiment | Optional (feature disabled if missing) |
| `FLASK_DEBUG`   | Enable debug mode          | No                                     |

## 🧠 Sentiment & Keywords

Sentiment (TextBlob polarity): `>0` positive, `=0` neutral, `<0` negative.
Keywords: filtered tokens (stopwords removed, alphanumeric, length>2) frequency top 10 per class.
Limitations: sarcasm, slang, named entities may skew results. Consider VADER / transformers for production.

## 🧭 Roadmap

-   [ ] Caching (Redis) for repeated titles
-   [ ] Transformer-based sentiment option
-   [ ] Better keyword extraction (bigrams, POS filtering)
-   [ ] PDF export of analysis
-   [ ] Public JSON API endpoints

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). PRs welcome.

## 🛡 Security

No real keys committed. See [SECURITY.md](SECURITY.md).

##
