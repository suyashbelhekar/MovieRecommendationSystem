import requests
import os
from config import TMDB_API_KEY, TMDB_BASE_URL, TMDB_IMAGE_BASE_URL

class TMDBIntegration:
    def __init__(self):
        self.api_key = TMDB_API_KEY
        self.base_url = TMDB_BASE_URL
        self.image_base_url = TMDB_IMAGE_BASE_URL
        
    def search_movie(self, title, year=None):
        """Search for a movie on TMDB"""
        if self.api_key == 'your_api_key_here':
            return None
            
        try:
            search_url = f"{self.base_url}/search/movie"
            params = {
                'api_key': self.api_key,
                'query': title,
                'year': year
            }
            
            response = requests.get(search_url, params=params)
            data = response.json()
            
            if data['results']:
                return data['results'][0]
            return None
            
        except Exception as e:
            print(f"Error searching movie: {str(e)}")
            return None
    
    def get_movie_poster(self, title, year=None):
        """Get movie poster URL"""
        movie_data = self.search_movie(title, year)
        if movie_data and movie_data.get('poster_path'):
            return f"{self.image_base_url}{movie_data['poster_path']}"
        return None
    
    def get_movie_details(self, title, year=None):
        """Get detailed movie information"""
        movie_data = self.search_movie(title, year)
        if not movie_data:
            return None
            
        try:
            # Get additional details
            movie_id = movie_data['id']
            details_url = f"{self.base_url}/movie/{movie_id}"
            params = {'api_key': self.api_key}
            
            response = requests.get(details_url, params=params)
            details = response.json()
            
            return {
                'title': details.get('title', title),
                'overview': details.get('overview', ''),
                'poster_url': f"{self.image_base_url}{details.get('poster_path', '')}" if details.get('poster_path') else None,
                'backdrop_url': f"{self.image_base_url}{details.get('backdrop_path', '')}" if details.get('backdrop_path') else None,
                'release_date': details.get('release_date', ''),
                'runtime': details.get('runtime', 0),
                'vote_average': details.get('vote_average', 0),
                'vote_count': details.get('vote_count', 0),
                'genres': [genre['name'] for genre in details.get('genres', [])],
                'production_companies': [company['name'] for company in details.get('production_companies', [])],
                'spoken_languages': [lang['name'] for lang in details.get('spoken_languages', [])]
            }
            
        except Exception as e:
            print(f"Error getting movie details: {str(e)}")
            return None
    
    def get_movie_trailer(self, title, year=None):
        """Get movie trailer URL"""
        movie_data = self.search_movie(title, year)
        if not movie_data:
            return None
            
        try:
            movie_id = movie_data['id']
            videos_url = f"{self.base_url}/movie/{movie_id}/videos"
            params = {'api_key': self.api_key}
            
            response = requests.get(videos_url, params=params)
            videos = response.json()
            
            # Find trailer
            for video in videos.get('results', []):
                if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
                    return f"https://www.youtube.com/watch?v={video['key']}"
            
            return None
            
        except Exception as e:
            print(f"Error getting trailer: {str(e)}")
            return None
    
    def get_trending_movies(self, limit=10):
        """Get trending movies"""
        if self.api_key == 'your_api_key_here':
            return []
            
        try:
            trending_url = f"{self.base_url}/trending/movie/week"
            params = {'api_key': self.api_key}
            
            response = requests.get(trending_url, params=params)
            data = response.json()
            
            trending_movies = []
            for movie in data.get('results', [])[:limit]:
                trending_movies.append({
                    'title': movie.get('title', ''),
                    'overview': movie.get('overview', ''),
                    'poster_url': f"{self.image_base_url}{movie.get('poster_path', '')}" if movie.get('poster_path') else None,
                    'vote_average': movie.get('vote_average', 0),
                    'release_date': movie.get('release_date', ''),
                    'id': movie.get('id', 0)
                })
            
            return trending_movies
            
        except Exception as e:
            print(f"Error getting trending movies: {str(e)}")
            return []
    
    def is_api_configured(self):
        """Check if TMDB API is properly configured"""
        return self.api_key != 'your_api_key_here' and self.api_key is not None
