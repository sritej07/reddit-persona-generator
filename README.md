# Reddit User Persona Generator

A Python script that analyzes Reddit user profiles and generates detailed user personas using Google's Gemini 2.5 Flash. This tool scrapes a user's posts and comments, processes the data, and creates comprehensive personas with citations.

## Features

- **Reddit Data Scraping**: Extracts posts and comments from any public Reddit user
- **Intelligent Data Processing**: Filters and cleans content for better analysis
- **AI-Powered Persona Generation**: Uses Gemini 2.5 Flash to create detailed user personas
- **Citation System**: Every persona characteristic is backed by specific Reddit posts/comments
- **Multiple Output Formats**: Generates both human-readable text and JSON outputs

## Installation

1. **Clone the repository**:
```bash
git clone <your-repository-url>
cd reddit-persona-generator
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**:
   - Copy `.env.example` to `.env`
   - Fill in your API credentials (see Setup section below)

## Setup

### Reddit API Setup

1. Go to [Reddit App Preferences](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Fill in the form:
   - Name: Your app name
   - App type: Select "script"
   - Description: Optional
   - About URL: Leave blank
   - Redirect URI: http://localhost:8080 (required but not used)
4. Copy the Client ID (under the app name) and Client Secret

### GEMINI API Setup

1. Go to [Gemini API Keys](https://aistudio.google.com/apikey)
2. Create a new API key
3. Copy the API key

### Environment Configuration

Create a `.env` file in the project root:

```env
# Reddit API Configuration
REDDIT_CLIENT_ID=your_reddit_client_id_here
REDDIT_CLIENT_SECRET=your_reddit_client_secret_here
REDDIT_USER_AGENT=PersonaBot/1.0
REDDIT_USERNAME=your_reddit_username_here
REDDIT_PASSWORD=your_reddit_password_here

# GEMINI API Configuration
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage

### Basic Usage

```bash
python main.py https://www.reddit.com/user/kojied/
```

### Using just the username

```bash
python main.py kojied
```

### Test with sample users

```bash
python main.py --test
```

### Command Line Options

```bash
python main.py <profile_url> [options]

Options:
  --output-dir OUTPUT_DIR   Output directory for results (default: outputs)
  --max-posts MAX_POSTS     Maximum posts to scrape (default: 50)
  --max-comments MAX_COMMENTS Maximum comments to scrape (default: 50)
```

## Output

The script generates two files for each user:

1. **`username_persona.txt`**: Human-readable persona report
2. **`username_persona.json`**: Structured data backup

### Sample Output Structure

```
USER PERSONA REPORT FOR: kojied
Generated on: 2024-01-15 14:30:45

ACTIVITY SUMMARY:
- Total Posts: 45
- Total Comments: 49
- Average Post Score: 15.2
- Average Comment Score: 8.7
- Top 5 Subreddits: r/programming(23), r/python(15), r/MachineLearning(12)

# USER PERSONA

## DEMOGRAPHIC INFORMATION
**Age Range**: 25-35 years old
**Citations**: "I graduated college in 2015..." "When I was in my twenties..."

**Location**: United States, likely West Coast
**Citations**: "Living in SF is expensive..." "PST timezone works for me..."

## PERSONALITY TRAITS
**Communication Style**: Technical, helpful, direct
**Citations**: "Here's the solution to your problem..." "You should try this approach..."

[... more detailed persona information with citations ...]
```

## Project Structure

```
reddit-persona-generator/
├── main.py                 # Main execution script
├── scraper.py             # Reddit data scraping
├── data_processor.py      # Data cleaning and processing
├── persona_generator.py   # AI persona generation
├── utils.py               # Utility functions and output management
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
├── outputs/              # Generated persona files
│   ├── kojied_persona.txt
│   └── kojied_persona.json
└── data/                 # Raw scraped data (temporary)
    └── raw_data/
```

## How It Works

1. **Data Scraping**: Uses PRAW (Python Reddit API Wrapper) to collect user posts and comments
2. **Data Processing**: Filters out deleted/removed content, cleans text, and extracts metadata
3. **AI Analysis**: Sends processed data to Google's Gemini 2.5 Flash with a structured prompt
4. **Persona Generation**: AI analyzes patterns and generates comprehensive user personas
5. **Citation Extraction**: Maps each persona characteristic back to specific Reddit content
6. **Output Generation**: Creates formatted text files and JSON backups

## Configuration Options

Modify `config.py` to adjust:
- Maximum number of posts/comments to scrape
- Request delays to avoid rate limiting
- Output directories
- API timeouts and retry settings

## Error Handling

The script includes comprehensive error handling for:
- Invalid Reddit usernames
- Private or deleted profiles
- API rate limiting
- Network connectivity issues
- Missing environment variables

## Limitations

- Only works with public Reddit profiles
- Limited by Reddit API rate limits
- Requires GEMINI API credits
- Analysis quality depends on user's posting history

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is for educational purposes. Please respect user privacy and Reddit's terms of service.

## Support

For issues or questions:
1. Check the error messages for missing environment variables
2. Verify your API credentials are correct
3. Ensure the Reddit username exists and is public
4. Check your GEMINI API usage limits

## Sample Users for Testing

The assignment provides these sample users:
- https://www.reddit.com/user/kojied/
- https://www.reddit.com/user/Hungry-Move-6603/

Use the test command to run analysis on both:
```bash
python main.py --test
```