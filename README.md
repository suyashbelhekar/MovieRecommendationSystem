# Movie Recommendation System

A modern, interactive movie recommendation system built with machine learning and Streamlit.

## Features

- **Content-based Recommendation**: Uses TF-IDF + Cosine Similarity
- **Modern UI**: Hover animations, gradients, dark/light mode
- **Interactive Effects**: Balloons/confetti animations
- **TMDB Integration**: Real movie posters and trailers
- **Responsive Design**: Beautiful movie cards with ratings and genres

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

## Usage

1. Enter a movie title in the search bar
2. Get top 5 similar movie recommendations
3. View movie details with posters and ratings
4. Toggle between light and dark modes
5. Enjoy interactive animations!

## Dataset

The system works with any CSV dataset containing movie information. Required columns:
- title: Movie title
- genre: Movie genres
- overview: Movie description
- rating: Movie rating (optional)

## API Keys

For TMDB integration, add your API key to the `.env` file:
```
TMDB_API_KEY=your_api_key_here
```
