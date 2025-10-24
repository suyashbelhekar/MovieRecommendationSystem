import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import re
import os

class MovieRecommender:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.8
        )
        self.movies_df = None
        self.tfidf_matrix = None
        self.similarity_matrix = None
        
    def preprocess_data(self, csv_file):
        """
        Load and preprocess movie data from CSV file
        """
        try:
            # Load the dataset
            self.movies_df = pd.read_csv(csv_file)
            
            # Clean and preprocess the data
            self.movies_df = self.movies_df.dropna(subset=['title', 'overview'])
            
            # Create a combined feature for TF-IDF
            self.movies_df['combined_features'] = (
                self.movies_df['overview'].fillna('') + ' ' +
                self.movies_df['genre'].fillna('') + ' ' +
                self.movies_df['title'].fillna('')
            )
            
            # Clean the combined features
            self.movies_df['combined_features'] = self.movies_df['combined_features'].apply(
                lambda x: re.sub(r'[^a-zA-Z\s]', '', str(x).lower())
            )
            
            print(f"Loaded {len(self.movies_df)} movies successfully")
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            return False
    
    def build_model(self):
        """
        Build TF-IDF model and compute similarity matrix
        """
        try:
            # Fit TF-IDF vectorizer
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(
                self.movies_df['combined_features']
            )
            
            # Compute cosine similarity matrix
            self.similarity_matrix = cosine_similarity(self.tfidf_matrix)
            
            print("Model built successfully")
            return True
            
        except Exception as e:
            print(f"Error building model: {str(e)}")
            return False
    
    def get_recommendations(self, movie_title, top_n=5):
        """
        Get movie recommendations based on title
        """
        try:
            # Find the movie index
            movie_idx = self.movies_df[
                self.movies_df['title'].str.lower() == movie_title.lower()
            ].index
            
            if len(movie_idx) == 0:
                # Try partial matching
                movie_idx = self.movies_df[
                    self.movies_df['title'].str.lower().str.contains(
                        movie_title.lower(), na=False
                    )
                ].index
                
                if len(movie_idx) == 0:
                    return None, "Movie not found in database"
            
            # Get the first match
            movie_idx = movie_idx[0]
            
            # Get similarity scores
            similarity_scores = list(enumerate(self.similarity_matrix[movie_idx]))
            
            # Sort by similarity score
            similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
            
            # Get top N recommendations (excluding the movie itself)
            top_movies = similarity_scores[1:top_n+1]
            
            # Extract movie information
            recommendations = []
            for idx, score in top_movies:
                movie_info = {
                    'title': self.movies_df.iloc[idx]['title'],
                    'genre': self.movies_df.iloc[idx]['genre'],
                    'overview': self.movies_df.iloc[idx]['overview'],
                    'rating': self.movies_df.iloc[idx].get('rating', 'N/A'),
                    'year': self.movies_df.iloc[idx].get('year', 'N/A'),
                    'similarity_score': round(score, 3)
                }
                recommendations.append(movie_info)
            
            return recommendations, None
            
        except Exception as e:
            return None, f"Error getting recommendations: {str(e)}"
    
    def save_model(self, filename='model.pkl'):
        """
        Save the trained model
        """
        try:
            model_data = {
                'tfidf_vectorizer': self.tfidf_vectorizer,
                'tfidf_matrix': self.tfidf_matrix,
                'similarity_matrix': self.similarity_matrix,
                'movies_df': self.movies_df
            }
            
            with open(filename, 'wb') as f:
                pickle.dump(model_data, f)
            
            print(f"Model saved as {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving model: {str(e)}")
            return False
    
    def load_model(self, filename='model.pkl'):
        """
        Load a pre-trained model
        """
        try:
            with open(filename, 'rb') as f:
                model_data = pickle.load(f)
            
            self.tfidf_vectorizer = model_data['tfidf_vectorizer']
            self.tfidf_matrix = model_data['tfidf_matrix']
            self.similarity_matrix = model_data['similarity_matrix']
            self.movies_df = model_data['movies_df']
            
            print(f"Model loaded from {filename}")
            return True
            
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def get_movie_list(self):
        """
        Get list of all movies in the dataset
        """
        if self.movies_df is not None:
            return self.movies_df['title'].tolist()
        return []

def train_model(csv_file='sample_movies.csv', model_file='model.pkl'):
    """
    Train and save the movie recommendation model
    """
    recommender = MovieRecommender()
    
    # Load and preprocess data
    if not recommender.preprocess_data(csv_file):
        return False
    
    # Build model
    if not recommender.build_model():
        return False
    
    # Save model
    if not recommender.save_model(model_file):
        return False
    
    return True

if __name__ == "__main__":
    # Train the model
    success = train_model()
    if success:
        print("Model training completed successfully!")
    else:
        print("Model training failed!")
