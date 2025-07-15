import os
import json
from datetime import datetime
from typing import Dict
from config import OUTPUT_DIR

class OutputManager:
    def __init__(self):
        """Initialize output manager"""
        self.output_dir = OUTPUT_DIR
        os.makedirs(self.output_dir, exist_ok=True)
    
    def format_persona_output(self, persona_data: Dict, username: str) -> str:
        """Format persona data into readable text output"""
        output_lines = []
        
        # Header
        output_lines.append("=" * 60)
        output_lines.append(f"USER PERSONA REPORT FOR: {username}")
        output_lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output_lines.append("=" * 60)
        output_lines.append("")
        
        # Add metadata summary
        metadata = persona_data.get('metadata', {})
        output_lines.append("ACTIVITY SUMMARY:")
        output_lines.append(f"- Total Posts: {metadata.get('total_posts', 0)}")
        output_lines.append(f"- Total Comments: {metadata.get('total_comments', 0)}")
        output_lines.append(f"- Average Post Score: {metadata.get('avg_post_score', 0):.2f}")
        output_lines.append(f"- Average Comment Score: {metadata.get('avg_comment_score', 0):.2f}")
        
        if metadata.get('top_subreddits'):
            output_lines.append(f"- Top 5 Subreddits: {', '.join([f'r/{sub}({count})' for sub, count in metadata['top_subreddits'][:5]])}")
        
        output_lines.append("")
        output_lines.append("=" * 60)
        output_lines.append("")
        
        # Add the raw LLM response (which contains the formatted persona)
        raw_response = persona_data.get('raw_response', '')
        if raw_response:
            output_lines.append(raw_response)
        else:
            # Fallback: format structured data
            structured_data = persona_data.get('structured_data', {})
            for section, subsections in structured_data.items():
                output_lines.append(f"## {section}")
                output_lines.append("")
                
                for subsection, data in subsections.items():
                    output_lines.append(f"**{subsection}**: {data['content']}")
                    
                    if data['citations']:
                        output_lines.append("**Citations**:")
                        for citation in data['citations']:
                            output_lines.append(f"  - {citation}")
                    
                    output_lines.append("")
        
        return "\n".join(output_lines)
    
    def save_to_text_file(self, content: str, username: str) -> str:
        """Save formatted persona to text file"""
        filename = f"{username}_persona.txt"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"Persona saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving persona to file: {e}")
            return ""
    
    def save_json_backup(self, persona_data: Dict, username: str) -> str:
        """Save persona data as JSON backup"""
        filename = f"{username}_persona.json"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(persona_data, f, indent=2, ensure_ascii=False, default=str)
            
            print(f"JSON backup saved to: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error saving JSON backup: {e}")
            return ""

def extract_username_from_url(url: str) -> str:
    """Extract username from Reddit profile URL"""
    import re
    
    # Match various Reddit URL formats
    patterns = [
        r'reddit\.com/user/([^/]+)',
        r'reddit\.com/u/([^/]+)',
        r'www\.reddit\.com/user/([^/]+)',
        r'www\.reddit\.com/u/([^/]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # If no match, assume the input is already a username
    return url.strip('/')

def validate_environment() -> bool:
    """Validate that all required environment variables are set"""
    required_vars = [
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET',
        'GEMINI_API_KEY',
        'REDDIT_USERNAME',
        'REDDIT_PASSWORD'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    return True

def print_progress(step: str, total_steps: int, current_step: int):
    """Print progress indicator"""
    progress = (current_step / total_steps) * 100
    print(f"[{progress:.1f}%] {step}")

def handle_error(error: Exception, context: str):
    """Handle and log errors consistently"""
    print(f"ERROR in {context}: {str(error)}")
    print(f"Error type: {type(error).__name__}")
    
    # You could add logging here in a real implementation
    return False