import re
from datetime import datetime
from typing import Dict, List, Any


class DataProcessor:
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'this', 'that', 'these', 'those', 'i', 'me', 'my', 
            'we', 'our', 'you', 'your', 'he', 'him', 'his', 'she', 'her', 'it', 
            'its', 'they', 'them', 'their'
        }
    
    def filter_relevant_content(self, user_data: Dict) -> Dict:
        """Filter out irrelevant or low-quality content"""
        filtered_posts = []
        filtered_comments = []
        
        # Filter posts
        for post in user_data['posts']:
            # Skip deleted or removed posts
            if post['selftext'] in ['[deleted]', '[removed]', '']:
                continue
            
            # Skip posts with very low scores (might be spam)
            if post['score'] < -5:
                continue
            
            # Clean the text
            post['selftext'] = self.clean_text(post['selftext'])
            post['title'] = self.clean_text(post['title'])
            
            if len(post['selftext']) > 10 or len(post['title']) > 10:
                filtered_posts.append(post)
        
        # Filter comments
        for comment in user_data['comments']:
            # Skip deleted or removed comments
            if comment['body'] in ['[deleted]', '[removed]', '']:
                continue
            
            # Skip very short comments
            if len(comment['body']) < 10:
                continue
            
            # Skip comments with very low scores
            if comment['score'] < -5:
                continue
            
            # Clean the text
            comment['body'] = self.clean_text(comment['body'])
            
            if len(comment['body']) > 10:
                filtered_comments.append(comment)
        
        user_data['posts'] = filtered_posts
        user_data['comments'] = filtered_comments
        
        print(f"Filtered data: {len(filtered_posts)} posts, {len(filtered_comments)} comments")
        return user_data
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove URLs
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # Remove Reddit-specific formatting
        text = re.sub(r'/u/[A-Za-z0-9_-]+', '', text)  # Remove usernames
        text = re.sub(r'/r/[A-Za-z0-9_-]+', '', text)  # Remove subreddit links
        text = re.sub(r'\*\*([^*]+)\*\*', r'\\1', text)  # Remove bold formatting
        text = re.sub(r'\*([^*]+)\*', r'\\1', text)  # Remove italic formatting
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_metadata(self, user_data: Dict) -> Dict:
        """Extract metadata and statistics from user data"""
        posts = user_data['posts']
        comments = user_data['comments']
        
        # Subreddit activity
        subreddit_activity = {}
        for post in posts:
            subreddit = post['subreddit']
            subreddit_activity[subreddit] = subreddit_activity.get(subreddit, 0) + 1
        
        for comment in comments:
            subreddit = comment['subreddit']
            subreddit_activity[subreddit] = subreddit_activity.get(subreddit, 0) + 1
        
        # Sort subreddits by activity
        top_subreddits = sorted(subreddit_activity.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Activity patterns
        posting_times = []
        for post in posts:
            posting_times.append(datetime.fromtimestamp(post['created_utc']))
        
        for comment in comments:
            posting_times.append(datetime.fromtimestamp(comment['created_utc']))
        
        # Calculate average scores
        avg_post_score = sum(post['score'] for post in posts) / len(posts) if posts else 0
        avg_comment_score = sum(comment['score'] for comment in comments) / len(comments) if comments else 0
        
        metadata = {
            'total_posts': len(posts),
            'total_comments': len(comments),
            'top_subreddits': top_subreddits,
            'avg_post_score': avg_post_score,
            'avg_comment_score': avg_comment_score,
            'posting_times': posting_times,
            'most_active_subreddit': top_subreddits[0][0] if top_subreddits else None
        }
        
        return metadata
    
    def prepare_llm_input(self, user_data: Dict) -> str:
        """Prepare formatted text for LLM analysis"""
        posts = user_data['posts']
        comments = user_data['comments']
        metadata = self.extract_metadata(user_data)
        
        # Combine all text content
        all_content = []
        
        # Add posts
        for post in posts[:20]:  # Limit to most recent 20 posts
            content = f"POST: {post['title']}\n{post['selftext']}\n"
            content += f"Subreddit: {post['subreddit']}, Score: {post['score']}\n"
            content += f"Date: {datetime.fromtimestamp(post['created_utc']).strftime('%Y-%m-%d')}\n"
            content += "---\n"
            all_content.append(content)
        
        # Add comments
        for comment in comments[:30]:  # Limit to most recent 30 comments
            content = f"COMMENT: {comment['body']}\n"
            content += f"Subreddit: {comment['subreddit']}, Score: {comment['score']}\n"
            content += f"Date: {datetime.fromtimestamp(comment['created_utc']).strftime('%Y-%m-%d')}\n"
            if comment['submission_title']:
                content += f"In response to: {comment['submission_title']}\n"
            content += "---\n"
            all_content.append(content)
        
        # Add metadata summary
        metadata_text = f"""
USER ACTIVITY SUMMARY:
- Total Posts: {metadata['total_posts']}
- Total Comments: {metadata['total_comments']}
- Average Post Score: {metadata['avg_post_score']:.2f}
- Average Comment Score: {metadata['avg_comment_score']:.2f}
- Most Active Subreddit: {metadata['most_active_subreddit']}
- Top 5 Subreddits: {', '.join([f"{sub}({count})" for sub, count in metadata['top_subreddits'][:5]])}

CONTENT:
"""
        
        final_input = metadata_text + "\n".join(all_content)
        
        return final_input
    
    def process_user_data(self, user_data: Dict) -> Dict:
        """Complete data processing pipeline"""
        print("Processing user data...")
        
        # Filter content
        filtered_data = self.filter_relevant_content(user_data)
        
        # Extract metadata
        metadata = self.extract_metadata(filtered_data)
        
        # Prepare LLM input
        llm_input = self.prepare_llm_input(filtered_data)
        
        processed_data = {
            'user_data': filtered_data,
            'metadata': metadata,
            'llm_input': llm_input
        }
        
        print("Data processing completed")
        return processed_data
