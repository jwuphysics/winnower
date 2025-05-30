"""Core processing logic for The Winnower."""

import os
from pathlib import Path
from typing import Dict, List, Optional

from .parsers import PaperParser
from .extractors import TechnicalExtractor
from .formatters import MarkdownFormatter


class WinnowerProcessor:
    """Main processor for extracting technical details from papers."""
    
    def __init__(self, config: Dict, model_provider: str = "openai", verbose: bool = False):
        self.config = config
        self.verbose = verbose
        
        self.parser = PaperParser(verbose=verbose)
        self.extractor = TechnicalExtractor(
            model_provider=model_provider,
            config=config,
            verbose=verbose
        )
        self.formatter = MarkdownFormatter()
    
    def process(self, input_source: str, output_dir: Path, recursive: bool = False) -> None:
        """Process papers and generate technical summaries."""
        papers = self._collect_papers(input_source, recursive)
        
        if not papers:
            print("No papers found to process.")
            return
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for paper_source in papers:
            try:
                if self.verbose:
                    print(f"\nProcessing: {paper_source}")
                
                paper_data = self.parser.parse(str(paper_source))
                technical_content = self.extractor.extract(paper_data)
                markdown_output = self.formatter.format(technical_content)
                
                output_file = self._generate_output_filename(paper_data, output_dir)
                output_file.write_text(markdown_output, encoding='utf-8')
                
                print(f"Generated: {output_file}")
                
            except Exception as e:
                print(f"Error processing {paper_source}: {e}")
                if self.verbose:
                    import traceback
                    traceback.print_exc()
    
    def _collect_papers(self, input_source: str, recursive: bool) -> List[str]:
        """Collect papers to process from input source."""
        source_path = Path(input_source)
        
        if source_path.is_file():
            return [input_source]
        elif source_path.is_dir():
            files = self.parser.find_papers_in_directory(source_path, recursive)
            return [str(f) for f in files]
        else:
            return [input_source]
    
    def _generate_output_filename(self, paper_data: Dict, output_dir: Path) -> Path:
        """Generate output filename for processed paper."""
        title = paper_data['title']
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_title = safe_title.replace(' ', '_')[:50]
        
        if not safe_title:
            safe_title = "paper"
        
        return output_dir / f"{safe_title}_technical_summary.md"