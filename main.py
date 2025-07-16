#!/usr/bin/env python3
"""
Reddit User Persona Generator
Scrapes Reddit user data and generates detailed user personas using GEMINI 2.5 Flash
"""

import sys
import argparse
from scraper import RedditScraper
from data_processor import DataProcessor
from persona_generator import PersonaGenerator
from utils import OutputManager, extract_username_from_url, validate_environment, print_progress, handle_error

def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(description='Generate user persona from Reddit profile')
    parser.add_argument('profile_url', help='Reddit profile URL or username')
    parser.add_argument('--output-dir', default='outputs', help='Output directory for results')
    parser.add_argument('--max-posts', type=int, default=100, help='Maximum posts to scrape')
    parser.add_argument('--max-comments', type=int, default=200, help='Maximum comments to scrape')
    
    args = parser.parse_args()
    
    # Validate environment
    if not validate_environment():
        print("Please set up your environment variables in a .env file:")
        print("REDDIT_CLIENT_ID=your_client_id")
        print("REDDIT_CLIENT_SECRET=your_client_secret")
        print("REDDIT_USER_AGENT=YourApp/1.0")
        print("REDDIT_USERNAME=your_reddit_username")
        print("REDDIT_PASSWORD=your_reddit_password")
        print("GEMINI_API_KEY=your_GEMINI_api_key")
        return False
    
    # Extract username from URL
    username = extract_username_from_url(args.profile_url)
    print(f"Processing Reddit user: {username}")
    print("=" * 50)
    
    try:
        # Initialize components
        scraper = RedditScraper()
        processor = DataProcessor()
        generator = PersonaGenerator()
        output_manager = OutputManager()
        
        # Step 1: Scrape user data
        print_progress("Scraping Reddit user data...", 4, 1)
        user_data = scraper.scrape_user_profile(username)
        
        if not user_data['posts'] and not user_data['comments']:
            print("No data found for this user. User may not exist or have no public posts/comments.")
            return False
        
        # Step 2: Process the data
        print_progress("Processing and cleaning data...", 4, 2)
        processed_data = processor.process_user_data(user_data)
        
        # Step 3: Generate persona
        print_progress("Generating user persona with AI...", 4, 3)
        persona_data = generator.generate_persona(processed_data)
        
        # Step 4: Save output
        print_progress("Saving results...", 4, 4)
        
        # Format and save text output
        formatted_output = output_manager.format_persona_output(persona_data, username)
        text_file = output_manager.save_to_text_file(formatted_output, username)
        
        # Save JSON backup
        json_file = output_manager.save_json_backup(persona_data, username)
        
        # Success message
        print("\n" + "=" * 50)
        print("SUCCESS! Persona generation completed.")
        print(f"Text output: {text_file}")
        print(f"JSON backup: {json_file}")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        handle_error(e, "main execution")
        return False

def test_with_sample_users():
    """Test the script with provided sample users"""
    sample_users = [
        "https://www.reddit.com/user/kojied/",
        "https://www.reddit.com/user/Hungry-Move-6603/"
    ]
    
    print("Testing with sample users...")
    success_count = 0
    
    for url in sample_users:
        username = extract_username_from_url(url)
        print(f"\nTesting with user: {username}")
        
        if main_with_url(url):
            success_count += 1
            print(f"✓ Success for {username}")
        else:
            print(f"✗ Failed for {username}")
    
    print(f"\nTest Results: {success_count}/{len(sample_users)} successful")
    return success_count == len(sample_users)

def main_with_url(url: str) -> bool:
    """Helper function to run main with a specific URL"""
    import sys
    original_argv = sys.argv
    sys.argv = ['main.py', url]
    
    try:
        result = main()
        return result
    finally:
        sys.argv = original_argv

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python main.py <reddit_profile_url>")
        print("Example: python main.py https://www.reddit.com/user/kojied/")
        print("\nOr run with --test to test sample users:")
        print("python main.py --test")
        sys.exit(1)
    
    if "--test" in sys.argv:
        test_with_sample_users()
    else:
        main()