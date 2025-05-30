"""Technical content extraction using AI models."""

import os
import re
from typing import Dict, List, Optional

try:
    import openai
except ImportError:
    openai = None

try:
    import anthropic
except ImportError:
    anthropic = None


class TechnicalExtractor:
    """Extract technical content from papers using AI models."""
    
    EXTRACTION_PROMPT = """
You are a technical reviewer tasked with extracting the core technical details from a research paper. 

Focus on extracting:
1. **Core Methods**: The fundamental approaches, algorithms, or techniques
2. **Technical Implementation**: Specific algorithms, mathematical formulations, architectural details
3. **Key Innovations**: Novel technical contributions or improvements
4. **Technical Parameters**: Important hyperparameters, model configurations, technical specifications
5. **Experimental Setup**: Technical aspects of experiments (not results/benchmarks)

IGNORE:
- Marketing language and promotional content
- Extensive benchmark comparisons and results tables
- Related work sections (unless they contain technical details for the current work)
- General background information
- Detailed experimental results and performance metrics

Extract the information and structure it with clear headings. Be concise but comprehensive for technical details.

Paper Title: {title}

Paper Content:
{content}

Extract the technical details following the structure above:
"""
    
    def __init__(self, model_provider: str = "openai", config: Dict = None, verbose: bool = False):
        self.model_provider = model_provider
        self.config = config or {}
        self.verbose = verbose
        
        if model_provider == "openai":
            if not openai:
                raise ImportError("OpenAI package not installed. Run: pip install openai")
            self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        elif model_provider == "anthropic":
            if not anthropic:
                raise ImportError("Anthropic package not installed. Run: pip install anthropic")
            self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        else:
            raise ValueError(f"Unsupported model provider: {model_provider}")
    
    def extract(self, paper_data: Dict) -> Dict:
        """Extract technical content from paper data."""
        if self.verbose:
            print("Extracting technical content...")
        
        content = self._preprocess_content(paper_data['content'])
        
        if len(content) > 100000:
            content = content[:100000] + "\n[Content truncated for processing]"
        
        technical_content = self._extract_with_ai(paper_data['title'], content)
        
        return {
            'title': paper_data['title'],
            'authors': paper_data['authors'],
            'source': paper_data['source'],
            'url': paper_data['url'],
            'abstract': paper_data['abstract'],
            'technical_content': technical_content,
        }
    
    def _preprocess_content(self, content: str) -> str:
        """Clean and preprocess paper content."""
        content = re.sub(r'\n+', '\n', content)
        content = re.sub(r'\s+', ' ', content)
        
        sections_to_remove = [
            r'References\s*\n.*',
            r'Bibliography\s*\n.*',
            r'Acknowledgments?\s*\n.*',
            r'Appendix\s*[A-Z]?\s*\n.*',
        ]
        
        for pattern in sections_to_remove:
            content = re.sub(pattern, '', content, flags=re.DOTALL | re.IGNORECASE)
        
        return content.strip()
    
    def _extract_with_ai(self, title: str, content: str) -> str:
        """Extract technical content using AI model."""
        prompt = self.EXTRACTION_PROMPT.format(title=title, content=content)
        
        if self.model_provider == "openai":
            return self._extract_with_openai(prompt)
        elif self.model_provider == "anthropic":
            return self._extract_with_anthropic(prompt)
    
    def _extract_with_openai(self, prompt: str) -> str:
        """Extract using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.config.get('openai_model', 'gpt-4'),
                messages=[
                    {"role": "system", "content": "You are a technical reviewer extracting core technical details from research papers."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.config.get('max_tokens', 4000),
                temperature=self.config.get('temperature', 0.1),
            )
            return response.choices[0].message.content
        except Exception as e:
            if self.verbose:
                print(f"OpenAI API error: {e}")
            return f"Error extracting technical content: {e}"
    
    def _extract_with_anthropic(self, prompt: str) -> str:
        """Extract using Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.config.get('anthropic_model', 'claude-3-sonnet-20240229'),
                max_tokens=self.config.get('max_tokens', 4000),
                temperature=self.config.get('temperature', 0.1),
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            if self.verbose:
                print(f"Anthropic API error: {e}")
            return f"Error extracting technical content: {e}"