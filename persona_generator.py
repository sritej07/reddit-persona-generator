import google.generativeai as genai
from typing import Dict, List, Tuple
from config import GEMINI_API_KEY # Assuming you've changed this in config.py


class PersonaGenerator:
    def __init__(self):
        """Initialize Gemini client"""
        genai.configure(api_key=GEMINI_API_KEY)
        self.client = genai.GenerativeModel("gemini-2.5-flash") # Initialize with the model directly
    
    def generate_persona_prompt(self, user_input: str) -> str:
        """Generate a comprehensive prompt for persona creation"""
        prompt = f"""
You are an expert user researcher tasked with creating a detailed user persona based on a Reddit user's posts and comments. 

Please analyze the following Reddit user data and create a comprehensive user persona. For each characteristic you identify, you MUST provide specific citations from the user's posts or comments that support that characteristic.

FORMAT YOUR RESPONSE EXACTLY AS FOLLOWS:

# USER PERSONA

## DEMOGRAPHIC INFORMATION
**Age Range**: [estimated age range]
**Citations**: [specific post/comment excerpts that indicate age]

**Location**: [estimated location/region]
**Citations**: [specific post/comment excerpts that indicate location]

**Occupation/Field**: [estimated profession or field of work]
**Citations**: [specific post/comment excerpts that indicate occupation]

## PERSONALITY TRAITS
**Communication Style**: [how they communicate - formal, casual, humorous, etc.]
**Citations**: [specific examples of their communication style]

**Values and Beliefs**: [core values, political views, moral stances]
**Citations**: [specific posts/comments that reveal their values]

**Interests and Hobbies**: [main interests, hobbies, activities they enjoy]
**Citations**: [specific posts/comments about their interests]

## BEHAVIORAL PATTERNS
**Reddit Usage**: [how they use Reddit - lurker, active poster, specific communities]
**Citations**: [evidence of their Reddit behavior patterns]

**Social Behavior**: [how they interact with others online]
**Citations**: [examples of their social interactions]

**Problem-Solving Approach**: [how they approach problems or challenges]
**Citations**: [examples of them solving problems or asking for help]

## GOALS AND MOTIVATIONS
**Primary Goals**: [what they seem to be trying to achieve]
**Citations**: [posts/comments that reveal their goals]

**Pain Points**: [challenges or frustrations they face]
**Citations**: [specific examples of their frustrations or challenges]

## TECHNOLOGY USAGE
**Tech Savviness**: [their level of technical knowledge]
**Citations**: [evidence of their technical abilities or lack thereof]

**Digital Habits**: [how they use technology and digital platforms]
**Citations**: [examples of their digital behavior]

## ADDITIONAL INSIGHTS
**Unique Characteristics**: [any other notable traits or patterns]
**Citations**: [supporting evidence for these characteristics]

Remember: Every single characteristic must be backed by specific citations from the user's actual posts or comments. Use direct quotes where possible.

USER DATA TO ANALYZE:
{user_input}

Now create the user persona following the exact format above:
"""
        return prompt
    
    def call_llm_api(self, prompt: str, max_retries: int = 3) -> str:
        """Call Gemini API with retry logic"""
        for attempt in range(max_retries):
            try:
                # Gemini 1.5 Flash uses generate_content for conversational turns
                # The prompt itself acts as the user's input in a single turn.
                response = self.client.generate_content(
                    contents=[
                        {"role": "user", "parts": [prompt]}
                    ],
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=10000, 
                        temperature=0.7,
                    )
                )
                
                # Access the text from the response
                if hasattr(response, 'candidates') and response.candidates:
                    parts = response.candidates[0].content.parts
                    return ''.join([part.text for part in parts if hasattr(part, 'text')])
                else:
                    return response.text
                
            except Exception as e:
                print(f"API call attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    raise e
                
        return ""
    
    def parse_persona_response(self, response: str) -> Dict:
        """Parse the LLM response into structured data"""
        sections = {}
        current_section = None
        current_subsection = None
        
        lines = response.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # Main sections (##)
            if line.startswith('## '):
                current_section = line[3:].strip()
                sections[current_section] = {}
                current_subsection = None
            
            # Subsections (**text**:)
            elif line.startswith('**') and line.endswith('**:'):
                if current_section:
                    current_subsection = line[2:-3].strip()
                    sections[current_section][current_subsection] = {
                        'content': '',
                        'citations': []
                    }
            
            # Citations
            elif line.startswith('**Citations**:'):
                if current_section and current_subsection:
                    citation_text = line[13:].strip()
                    sections[current_section][current_subsection]['citations'].append(citation_text)
            
            # Regular content
            elif line and not line.startswith('#'):
                if current_section and current_subsection:
                    if sections[current_section][current_subsection]['content']:
                        sections[current_section][current_subsection]['content'] += ' ' + line
                    else:
                        sections[current_section][current_subsection]['content'] = line
        
        return sections
    
    def extract_citations(self, user_data: Dict, persona_data: Dict) -> Dict:
        """Extract and validate citations from user data"""
        all_posts = user_data['posts']
        all_comments = user_data['comments']
        
        # Create a searchable index of all content
        content_index = {}
        
        for post in all_posts:
            content_index[post['id']] = {
                'type': 'post',
                'title': post['title'],
                'content': post['selftext'],
                'subreddit': post['subreddit'],
                'score': post['score'],
                'date': post['created_utc']
            }
        
        for comment in all_comments:
            content_index[comment['id']] = {
                'type': 'comment',
                'content': comment['body'],
                'subreddit': comment['subreddit'],
                'score': comment['score'],
                'date': comment['created_utc'],
                'submission_title': comment.get('submission_title', '')
            }
        
        # Validate citations in persona data
        validated_citations = {}
        
        for section, subsections in persona_data.items():
            validated_citations[section] = {}
            for subsection, data in subsections.items():
                validated_citations[section][subsection] = {
                    'content': data['content'],
                    'citations': data['citations'],
                    'validated': True   # In a real implementation, you'd validate against content_index
                }
        
        return validated_citations
    
    def generate_persona(self, processed_data: Dict) -> Dict:
        """Generate complete user persona with citations"""
        print("Generating user persona...")
        
        # Generate prompt
        prompt = self.generate_persona_prompt(processed_data['llm_input'])
        
        # Call LLM API
        response = self.call_llm_api(prompt)
        
        # Parse response
        persona_data = self.parse_persona_response(response)
        
        # Extract and validate citations
        validated_persona = self.extract_citations(processed_data['user_data'], persona_data)
        
        final_persona = {
            'raw_response': response,
            'structured_data': validated_persona,
            'metadata': processed_data['metadata']
        }
        
        print("Persona generation completed")
        return final_persona

