import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# TMDB API Configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'your_api_key_here')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

# App Configuration
APP_TITLE = "🎬 Movie Recommendation System"
APP_ICON = "🎬"
APP_LAYOUT = "wide"

# Model Configuration
MODEL_FILE = 'model.pkl'
SAMPLE_DATA_FILE = 'sample_movies.csv'

# UI Configuration
DEFAULT_RECOMMENDATIONS = 5
MAX_RECOMMENDATIONS = 10
