# 🎬 Movie Recommendation System - Setup Guide

## Quick Start

### Option 1: Automatic Setup (Recommended)
1. **Windows Users**: Double-click `run_app.bat`
2. **All Users**: Run `python run_app.py`

### Option 2: Manual Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Train the model: `python movie_recommender.py`
3. Run the app: `streamlit run app_enhanced.py`

## Features

### ✅ Core Features
- **Content-based Recommendation**: Uses TF-IDF + Cosine Similarity
- **Modern UI**: Beautiful gradient backgrounds and animations
- **Interactive Effects**: Hover animations, confetti effects
- **Dark/Light Mode**: Toggle between themes
- **Movie Cards**: Display with ratings, genres, and overviews

### ✅ Advanced Features
- **TMDB Integration**: Real movie posters and trailers
- **Watchlist**: Save movies you want to watch
- **Trending Movies**: See what's popular
- **Random Movie**: Discover something new
- **Responsive Design**: Works on all devices

## TMDB API Setup (Optional)

For movie posters and trailers:

1. Get API key from: https://www.themoviedb.org/settings/api
2. Create `.env` file:
   ```
   TMDB_API_KEY=your_api_key_here
   ```
3. Restart the application

## File Structure

```
Movierecommend/
├── app.py                 # Basic Streamlit app
├── app_enhanced.py        # Enhanced app with TMDB integration
├── movie_recommender.py   # ML model and training
├── tmdb_integration.py    # TMDB API integration
├── config.py             # Configuration settings
├── sample_movies.csv     # Sample movie dataset
├── model.pkl            # Trained ML model
├── requirements.txt      # Python dependencies
├── run_app.py           # Application launcher
├── run_app.bat          # Windows batch file
└── README.md            # Project documentation
```

## Usage

1. **Search Movies**: Enter a movie title
2. **Get Recommendations**: See 5 similar movies
3. **Add to Watchlist**: Save movies for later
4. **View Posters**: See movie posters (with TMDB API)
5. **Watch Trailers**: Click to watch trailers
6. **Toggle Theme**: Switch between light/dark modes

## Customization

### Adding Your Own Dataset
1. Replace `sample_movies.csv` with your data
2. Ensure columns: `title`, `genre`, `overview`, `rating`, `year`
3. Retrain model: `python movie_recommender.py`

### Styling
- Edit CSS in `app_enhanced.py`
- Modify colors, fonts, and animations
- Add your own branding

## Troubleshooting

### Common Issues

1. **Model not found**: Run `python movie_recommender.py`
2. **Dependencies missing**: Run `pip install -r requirements.txt`
3. **TMDB API errors**: Check your API key in `.env`
4. **Port already in use**: Change port in `run_app.py`

### Performance Tips

1. **Large datasets**: Consider reducing TF-IDF features
2. **Memory usage**: Limit recommendations to 5-10 movies
3. **API calls**: Cache TMDB responses for better performance

## Support

- Check the console for error messages
- Ensure all dependencies are installed
- Verify your dataset format matches requirements
- Test with the sample dataset first

## Next Steps

- Add user authentication
- Implement collaborative filtering
- Add movie reviews and ratings
- Create user profiles
- Add social features

Happy movie watching! 🍿
