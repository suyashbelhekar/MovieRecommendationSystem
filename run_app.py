#!/usr/bin/env python3
"""
Movie Recommendation System Launcher
Run this script to start the application
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'requests',
        'PIL',
        'plotly'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed!")
    else:
        print("✅ All dependencies are installed!")

def check_model():
    """Check if model file exists"""
    if not os.path.exists('model.pkl'):
        print("🤖 Model not found. Training model...")
        subprocess.check_call([sys.executable, "movie_recommender.py"])
        print("✅ Model trained and saved!")
    else:
        print("✅ Model file found!")

def main():
    """Main launcher function"""
    print("🎬 Movie Recommendation System Launcher")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Check model
    check_model()
    
    print("\n🚀 Starting the application...")
    print("📱 Open your browser and go to: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop the application")
    print("=" * 50)
    
    # Start Streamlit app
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "app_enhanced.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped. Goodbye!")

if __name__ == "__main__":
    main()
