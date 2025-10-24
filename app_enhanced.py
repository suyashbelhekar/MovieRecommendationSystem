import streamlit as st
import pandas as pd
import numpy as np
import requests
import json
import time
import random
from movie_recommender import MovieRecommender
from tmdb_integration import TMDBIntegration
import os
from PIL import Image
import base64
from config import *

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=APP_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI with enhanced features
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
        position: relative;
        overflow: hidden;
    }
    
    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/><circle cx="10" cy="60" r="0.5" fill="white" opacity="0.1"/><circle cx="90" cy="40" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
    }
    
    .header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        position: relative;
        z-index: 1;
    }
    
    .header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
        position: relative;
        z-index: 1;
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
    
    /* Trending Movies Section */
    .trending-section {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        color: white;
    }
    
    .trending-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .trending-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.2);
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
        to { transform: rotate(360deg); }
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
    
    /* Watchlist Styles */
    .watchlist-item {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .watchlist-item:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateX(5px);
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
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'tmdb' not in st.session_state:
    st.session_state.tmdb = TMDBIntegration()

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
            if os.path.exists(MODEL_FILE):
                if recommender.load_model(MODEL_FILE):
                    st.session_state.recommender = recommender
                    return True
            else:
                st.error("Model file not found. Please train the model first.")
                return False
        except Exception as e:
            st.error(f"Error loading model: {str(e)}")
            return False
    return True

def add_to_watchlist(movie_title):
    """Add movie to watchlist"""
    if movie_title not in st.session_state.watchlist:
        st.session_state.watchlist.append(movie_title)
        st.success(f"✅ Added '{movie_title}' to watchlist!")

def remove_from_watchlist(movie_title):
    """Remove movie from watchlist"""
    if movie_title in st.session_state.watchlist:
        st.session_state.watchlist.remove(movie_title)
        st.success(f"🗑️ Removed '{movie_title}' from watchlist!")

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
        
        # TMDB Status
        st.markdown("### 🎬 TMDB Integration")
        if st.session_state.tmdb.is_api_configured():
            st.success("✅ TMDB API Connected")
        else:
            st.warning("⚠️ TMDB API not configured")
            st.info("Add your TMDB API key to get movie posters and trailers")
        
        # Watchlist Section
        st.markdown("### 📝 My Watchlist")
        if st.session_state.watchlist:
            for movie in st.session_state.watchlist:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"🎬 {movie}")
                with col2:
                    if st.button("🗑️", key=f"remove_{movie}"):
                        remove_from_watchlist(movie)
        else:
            st.info("No movies in watchlist yet")
    
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
                            movie_input, top_n=DEFAULT_RECOMMENDATIONS
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
    
    # Trending Movies Section
    if st.session_state.tmdb.is_api_configured():
        st.markdown("## 🔥 Trending Movies")
        
        if st.button("🔄 Refresh Trending"):
            with st.spinner("Loading trending movies..."):
                trending_movies = st.session_state.tmdb.get_trending_movies(limit=5)
                
                if trending_movies:
                    cols = st.columns(len(trending_movies))
                    for i, movie in enumerate(trending_movies):
                        with cols[i]:
                            st.markdown(f"""
                            <div class="trending-card">
                                <h4>🎬 {movie['title']}</h4>
                                <p>⭐ {movie['vote_average']}/10</p>
                                <p>📅 {movie['release_date']}</p>
                            </div>
                            """, unsafe_allow_html=True)
                            
                            if movie['poster_url']:
                                st.image(movie['poster_url'], width=100)
    
    # Display Recommendations
    if st.session_state.recommendations:
        st.markdown("## 🎬 Your Recommendations")
        
        for i, movie in enumerate(st.session_state.recommendations, 1):
            with st.container():
                col1, col2, col3 = st.columns([1, 3, 1])
                
                with col1:
                    # Try to get movie poster
                    poster_url = st.session_state.tmdb.get_movie_poster(movie['title'], movie.get('year'))
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
                
                with col3:
                    if st.button(f"📝 Add to Watchlist", key=f"add_{i}"):
                        add_to_watchlist(movie['title'])
                    
                    # Get trailer if TMDB is configured
                    if st.session_state.tmdb.is_api_configured():
                        trailer_url = st.session_state.tmdb.get_movie_trailer(movie['title'], movie.get('year'))
                        if trailer_url:
                            st.markdown(f"[🎥 Watch Trailer]({trailer_url})")
        
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
