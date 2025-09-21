# Contributing Guide

Thanks for considering contributing! This project was originally created as an educational / college project and is now evolving into a more production-quality learning resource for:

-   NLP + sentiment analysis with TextBlob / spaCy / NLTK
-   Web scraping (Letterboxd, Rotten Tomatoes, OMDb API) – for educational use only
-   Flask application architecture & data visualization (Plotly)

## Ways to Contribute

-   Fix bugs (see Issues)
-   Improve scraping reliability (respect robots.txt, add backoff)
-   Add tests / improve coverage
-   Improve model quality (experiment with VADER, transformers)
-   Optimize Docker image / deployment
-   Documentation & tutorials

## Development Setup

1. Fork & clone the repo
2. Create a virtual environment
3. Install dependencies: `pip install -r requirements.txt -r requirements-dev.txt`
4. Run the app: `python app.py`
5. Run tests: `pytest -q`

## Coding Standards

-   Python ≥ 3.10
-   Use type hints for new / modified functions
-   Run `ruff check --fix .` and `black .` before committing (formatting is enforced in CI)
-   Keep functions small & documented (docstring first)

## Git Hygiene

-   Create a feature branch: `feat/short-description`
-   Keep commits atomic & meaningful
-   Reference related issues in commit messages (e.g. `Fix #12: handle empty reviews`)
-   Rebase over merge where reasonable to keep history linear

## Submitting a PR

1. Ensure tests pass locally
2. Ensure CI is green
3. Add/update docs if behavior changes
4. Request review

## Security / API Keys

Do not commit real API keys. Use `.env` (see `.env.example`). Report sensitive issues privately.

## License

By contributing you agree your contributions are licensed under the MIT License.

Happy hacking!
