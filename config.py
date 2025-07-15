import os
from dotenv import load_dotenv

load_dotenv()

# Reddit API Configuration
REDDIT_CLIENT_ID = os.getenv('REDDIT_CLIENT_ID')
REDDIT_CLIENT_SECRET = os.getenv('REDDIT_CLIENT_SECRET')
REDDIT_USER_AGENT = os.getenv('REDDIT_USER_AGENT', 'PersonaBot/1.0')
REDDIT_PASSWORD = os.getenv('REDDIT_PASSWORD')
REDDIT_USERNAME = os.getenv('REDDIT_USERNAME')
# GEMINI Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Scraping Configuration
MAX_POSTS = 50
MAX_COMMENTS = 50
REQUEST_DELAY = 1  # seconds between requests

# Output Configuration
OUTPUT_DIR = 'outputs'
DATA_DIR = 'data'