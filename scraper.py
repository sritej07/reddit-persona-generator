import praw
import time
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from config import (
    REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT,
    MAX_POSTS, MAX_COMMENTS, REQUEST_DELAY, DATA_DIR
)

class RedditScraper:
    def __init__(self):
        """Initialize Reddit API client"""
        self.reddit = praw.Reddit(
            client_id=REDDIT_CLIENT_ID,
            client_secret=REDDIT_CLIENT_SECRET,
            user_agent=REDDIT_USER_AGENT,
            password="Sritej@15",
            username="gajala07"
        )
        self.reddit.read_only = True
    
    def setup_reddit_client(self) -> bool:
        """Test Reddit API connection"""
        try:
            # Test connection
            self.reddit.user.me()
            return True
        except Exception as e:
            print(f"Reddit API connection failed: {e}")
            return False
    
    def scrape_user_posts(self, username: str) -> List[Dict]:
        """Scrape posts from a Reddit user"""
        posts = []
        try:
            user = self.reddit.redditor(username)
            
            # Get user's submissions (posts)
            for submission in user.submissions.new(limit=MAX_POSTS):
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'selftext': submission.selftext,
                    'subreddit': str(submission.subreddit),
                    'created_utc': submission.created_utc,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'url': submission.url,
                    'is_self': submission.is_self,
                    'type': 'post'
                }
                posts.append(post_data)
                time.sleep(REQUEST_DELAY)
            
            print(f"Scraped {len(posts)} posts for user {username}")
            return posts
            
        except Exception as e:
            print(f"Error scraping posts for {username}: {e}")
            return []
    
    def scrape_user_comments(self, username: str) -> List[Dict]:
        """Scrape comments from a Reddit user"""
        comments = []
        try:
            user = self.reddit.redditor(username)
            
            # Get user's comments
            for comment in user.comments.new(limit=MAX_COMMENTS):
                comment_data = {
                    'id': comment.id,
                    'body': comment.body,
                    'subreddit': str(comment.subreddit),
                    'created_utc': comment.created_utc,
                    'score': comment.score,
                    'parent_id': comment.parent_id,
                    'submission_title': comment.submission.title if comment.submission else None,
                    'type': 'comment'
                }
                comments.append(comment_data)
                time.sleep(REQUEST_DELAY)
            
            print(f"Scraped {len(comments)} comments for user {username}")
            return comments
            
        except Exception as e:
            print(f"Error scraping comments for {username}: {e}")
            return []
    
    def save_raw_data(self, data: Dict, username: str) -> bool:
        """Save raw scraped data to JSON file"""
        try:
            # Create data directory if it doesn't exist
            os.makedirs(DATA_DIR, exist_ok=True)
            
            filename = os.path.join(DATA_DIR, f"{username}_raw_data.json")
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"Raw data saved to {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving raw data: {e}")
            return False
    
    def scrape_user_profile(self, username: str) -> Dict:
        """Complete scraping process for a user"""
        print(f"Starting to scrape profile for: {username}")
        
        # Scrape posts and comments
        posts = self.scrape_user_posts(username)
        comments = self.scrape_user_comments(username)
        
        # Combine all data
        user_data = {
            'username': username,
            'scraped_at': datetime.now().isoformat(),
            'posts': posts,
            'comments': comments,
            'total_posts': len(posts),
            'total_comments': len(comments)
        }
        
        # Save raw data
        self.save_raw_data(user_data, username)
        
        return user_data
