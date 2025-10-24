import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import time
import random
from movie_recommender import MovieRecommender
import os
from PIL import Image
import base64

# Page configuration
st.set_page_config(
    page_title="🎬 Movie Recommendation System",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Header Styles */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Search Container */
    .search-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* Movie Card Styles */
    .movie-card {
        background: linear-gradient(145deg, #ffffff, #f0f0f0);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .movie-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.2);
        background: linear-gradient(145deg, #f8f9ff, #e8f0ff);
    }
    
    .movie-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        border-radius: 20px 20px 0 0;
    }
    
    .movie-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .movie-genre {
        color: #667eea;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }
    
    .movie-rating {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .movie-overview {
        color: #4a5568;
        line-height: 1.6;
        margin-bottom: 1rem;
    }
    
    .similarity-score {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    /* Dark Mode Styles */
    [data-theme="dark"] .movie-card {
        background: linear-gradient(145deg, #2d3748, #1a202c);
        color: white;
    }
    
    [data-theme="dark"] .movie-card:hover {
        background: linear-gradient(145deg, #4a5568, #2d3748);
    }
    
    [data-theme="dark"] .movie-title {
        color: #e2e8f0;
    }
    
    [data-theme="dark"] .movie-overview {
        color: #a0aec0;
    }
    
    /* Confetti Animation */
    .confetti {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 1000;
    }
    
    .confetti-piece {
        position: absolute;
        width: 10px;
        height: 10px;
        background: #667eea;
        animation: confetti-fall 3s linear infinite;
    }
    
    @keyframes confetti-fall {
        0% {
            transform: translateY(-100vh) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: translateY(100vh) rotate(720deg);
            opacity: 0;
        }
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(102, 126, 234, 0.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg);
    }
    
    /* Sidebar Styles */
    .sidebar-content {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Success Message */
    .success-message {
        background: linear-gradient(135deg, #48bb78, #38a169);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    /* Error Message */
    .error-message {
        background: linear-gradient(135deg, #f56565, #e53e3e);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'recommender' not in st.session_state:
    st.session_state.recommender = None
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# TMDB API Configuration
TMDB_API_KEY = os.getenv('TMDB_API_KEY', 'your_api_key_here')
TMDB_BASE_URL = 'https://api.themoviedb.org/3'
TMDB_IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500'

def get_movie_poster(movie_title, year=None):
    """Get movie poster from TMDB API"""
    if TMDB_API_KEY == 'your_api_key_here':
        return None
    
    try:
        # Search for movie
        search_url = f"{TMDB_BASE_URL}/search/movie"
        params = {
            'api_key': TMDB_API_KEY,
            'query': movie_title,
            'year': year
        }
        
        response = requests.get(search_url, params=params)
        data = response.json()
        
        if data['results']:
            poster_path = data['results'][0]['poster_path']
            return f"{TMDB_IMAGE_BASE_URL}{poster_path}"
        
    except Exception as e:
        st.error(f"Error fetching poster: {str(e)}")
    
    return None

def create_confetti():
    """Create confetti animation"""
    confetti_html = """
    <div class="confetti" id="confetti">
        <div class="confetti-piece" style="left: 10%; animation-delay: 0s;"></div>
        <div class="confetti-piece" style="left: 20%; animation-delay: 0.1s;"></div>
        <div class="confetti-piece" style="left: 30%; animation-delay: 0.2s;"></div>
        <div class="confetti-piece" style="left: 40%; animation-delay: 0.3s;"></div>
        <div class="confetti-piece" style="left: 50%; animation-delay: 0.4s;"></div>
        <div class="confetti-piece" style="left: 60%; animation-delay: 0.5s;"></div>
        <div class="confetti-piece" style="left: 70%; animation-delay: 0.6s;"></div>
        <div class="confetti-piece" style="left: 80%; animation-delay: 0.7s;"></div>
        <div class="confetti-piece" style="left: 90%; animation-delay: 0.8s;"></div>
    </div>
    <script>
        setTimeout(() => {
            document.getElementById('confetti').remove();
        }, 3000);
    </script>
    """
    return confetti_html

def load_recommender():
    """Load the movie recommender model"""
    if st.session_state.recommender is None:
        try:
            recommender = MovieRecommender()
            if os.path.exists('model.pkl'):
                if recommender.load_model('model.pkl'):
                    st.session_state.recommender = recommender
                    return True
            else:
                st.error("Model file not found. Please train the model first.")
                return False
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return False
    return True

def main():
    # Header
    st.markdown("""
    <div class="header">
        <h1>🎬 Movie Recommendation System</h1>
        <p>Discover your next favorite movie with AI-powered recommendations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Navigation")
        
        # Dark/Light Mode Toggle
        if st.button("🌙 Toggle Dark Mode"):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
        
        st.markdown("---")
        
        # About Section
        st.markdown("""
        <div class="sidebar-content">
            <h3>📖 About</h3>
            <p>This movie recommendation system uses advanced machine learning techniques including TF-IDF vectorization and cosine similarity to provide personalized movie suggestions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Credits Section
        st.markdown("""
        <div class="sidebar-content">
            <h3>👨‍💻 Credits</h3>
            <p><strong>Built with:</strong></p>
            <ul>
                <li>Python & Streamlit</li>
                <li>Scikit-learn</li>
                <li>TF-IDF Vectorization</li>
                <li>Cosine Similarity</li>
                <li>TMDB API</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Model Status
        st.markdown("### 🔧 Model Status")
        if load_recommender():
            st.success("✅ Model Loaded")
            st.info(f"📊 {len(st.session_state.recommender.get_movie_list())} movies in database")
        else:
            st.error("❌ Model Not Loaded")
    
    # Main Content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="search-container">
            <h2>🔍 Find Your Next Movie</h2>
            <p>Enter a movie title to get personalized recommendations</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Search Input
        movie_input = st.text_input(
            "Enter a movie title:",
            placeholder="e.g., The Dark Knight, Inception, Pulp Fiction...",
            key="movie_search"
        )
        
        # Search Button
        if st.button("🎬 Get Recommendations", type="primary"):
            if movie_input:
                if load_recommender():
                    with st.spinner("🔍 Finding similar movies..."):
                        recommendations, error = st.session_state.recommender.get_recommendations(
                            movie_input, top_n=5
                        )
                        
                        if recommendations:
                            st.session_state.recommendations = recommendations
                            st.success("🎉 Recommendations found!")
                            
                            # Add confetti effect
                            st.markdown(create_confetti(), unsafe_allow_html=True)
                        else:
                            st.error(f"❌ {error}")
                else:
                    st.error("❌ Model not loaded. Please check the sidebar.")
            else:
                st.warning("⚠️ Please enter a movie title")
    
    with col2:
        st.markdown("### 🎲 Random Movie")
        if st.button("🎲 Get Random Movie"):
            if load_recommender():
                movies = st.session_state.recommender.get_movie_list()
                if movies:
                    random_movie = random.choice(movies)
                    st.info(f"🎬 Try: **{random_movie}**")
    
    # Display Recommendations
    if st.session_state.recommendations:
        st.markdown("## 🎬 Your Recommendations")
        
        for i, movie in enumerate(st.session_state.recommendations, 1):
            with st.container():
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    # Try to get movie poster
                    poster_url = get_movie_poster(movie['title'], movie.get('year'))
                    if poster_url:
                        st.image(poster_url, width=150, caption=movie['title'])
                    else:
                        st.markdown("🎬")
                
                with col2:
                    st.markdown(f"""
                    <div class="movie-card">
                        <div class="movie-title">#{i} {movie['title']}</div>
                        <div class="movie-genre">🎭 {movie['genre']}</div>
                        <div class="movie-rating">⭐ {movie['rating']}</div>
                        <div class="movie-overview">{movie['overview']}</div>
                        <div class="similarity-score">🎯 Similarity: {movie['similarity_score']}</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Clear recommendations button
        if st.button("🗑️ Clear Recommendations"):
            st.session_state.recommendations = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 2rem;">
        <p>🎬 Movie Recommendation System | Built with ❤️ using Streamlit & Machine Learning</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
