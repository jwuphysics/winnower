# CLAUDE.md - The Winnower

## Project Overview

The Winnower is a Python CLI tool designed to extract core technical details from research papers while filtering out benchmarks, promotional content, and marketing fluff. It processes papers from multiple input sources (local files, URLs, arXiv IDs, directories) and generates focused markdown summaries using AI models.

**Key Purpose**: Extract methods, algorithms, implementations, and technical specifications while ignoring:
- Extensive benchmark comparisons and results tables
- Marketing language and promotional content  
- Related work sections (unless containing technical details)
- General background information
- Detailed experimental results and performance metrics

**Target Users**: Researchers and developers who need technical implementation details without the noise.

**Primary Use Cases**:
1. **ML/Applied Math/Statistics**: Extract algorithms, core theoretical concepts that support understanding, mathematical formulations. Ignore benchmarks and non-generalizable applications.
2. **Physics/Astronomy**: Extract formulae, conceptual methods, theoretical frameworks. Focus on mathematical relationships and physical principles rather than specific computational implementations.

## Architecture

```
winnower/
├── winnower/                    # Main package
│   ├── cli.py                  # Command-line interface with argparse
│   ├── core.py                 # Main processing orchestration (WinnowerProcessor)
│   ├── parsers.py              # Input handling (PaperParser) - files, URLs, arXiv
│   ├── extractors.py           # AI-powered content extraction (TechnicalExtractor)
│   ├── formatters.py           # Markdown output generation (MarkdownFormatter)
│   ├── config.py               # Configuration management
│   ├── __init__.py             # Package metadata
│   └── prompts/                # Built-in extraction prompt templates
│       ├── ml_focused.txt      # ML/statistics domain
│       ├── physics_focused.txt # Physics/astronomy domain
│       ├── algorithms_focused.txt
│       ├── implementation_focused.txt
│       └── methods_summary.txt
├── tests/                       # Test suite
│   ├── fixtures/               # Test data (sample papers)
│   ├── test_smoke.py          # Basic functionality tests
│   ├── test_unit.py           # Unit tests
│   ├── test_integration.py    # End-to-end tests
│   └── conftest.py            # Test configuration
├── .github/workflows/          # CI/CD
├── pyproject.toml             # Package configuration
├── Makefile                   # Development commands
└── run_tests.py              # Test runner script
```

**Data Flow**:
1. CLI parses arguments and loads config
2. WinnowerProcessor orchestrates the pipeline
3. PaperParser handles input source and extracts raw content
4. TechnicalExtractor uses AI to identify and extract technical content
5. MarkdownFormatter generates structured output
6. Output saved as `{title}_technical_summary.md`

## Dependencies

**Core Dependencies**:
- `requests` - HTTP requests for URL fetching
- `beautifulsoup4` + `lxml` - HTML parsing
- `PyPDF2` - Legacy PDF text extraction (fallback)
- `pymupdf4llm` - Smart PDF to markdown conversion (primary)
- `arxiv` - arXiv API integration
- `openai` - OpenAI API (optional, one of two AI providers)
- `anthropic` - Anthropic API (optional, one of two AI providers)
- `python-dotenv` - Environment variable management

**Development Dependencies**:
- `pytest`, `pytest-cov` - Testing and coverage
- `black`, `flake8`, `mypy` - Code quality and formatting

**Testing Dependencies**:
- `pytest>=7.0.0`
- `pytest-cov>=4.0.0` - Coverage reporting

## Example Usage

```bash
# Setup
uv venv && source .venv/bin/activate
uv pip install -e .
winnower setup  # Creates ~/.winnower/.env template
# Edit ~/.winnower/.env to add API key

# Process single arXiv paper
winnower 2501.00089

# Process from URL
winnower https://arxiv.org/abs/2501.00089

# Process local file with custom output
winnower paper.pdf -o summaries/

# Process directory recursively with Anthropic
winnower /papers/ --recursive --model anthropic

# Use domain-specific prompts
winnower ml_paper.pdf --prompt-file winnower/prompts/ml_focused.txt
winnower physics_paper.pdf --prompt-file winnower/prompts/physics_focused.txt

# Verbose output with custom config
winnower paper.pdf --config my-config.json --verbose
```

## Configuration

**Configuration Priority** (highest to lowest):
1. Command-line arguments
2. Environment variables (WINNOWER_*)
3. Project .env file (current directory)
4. Global .env file (~/.winnower/.env)
5. Config file (--config or ~/.winnower/config.json)
6. Default values

**API Key Management**:
The Winnower uses a secure hierarchy for API key management:
1. **Environment variables** (highest priority) - Good for CI/CD, Docker
2. **Project .env file** - For project-specific development
3. **Global .env file** (`~/.winnower/.env`) - Personal/system-wide settings
4. **Never stored in JSON config** - Security best practice

Use `winnower setup` to create the global configuration directory and `.env` template.

**Key Configuration Options**:
- `openai_model`: Default "gpt-4.1-mini-2025-04-14"
- `anthropic_model`: Default "claude-3-sonnet-20240229"
- `max_tokens`: Default 4000
- `temperature`: Default 0.1
- `extraction_prompt`: Custom extraction prompt text
- `prompt_file`: Path to custom prompt file
- `pdf_to_markdown`: Default true (enables PDF to markdown conversion)

**Environment Variables**:
- `OPENAI_API_KEY` / `ANTHROPIC_API_KEY` - Required for AI processing
- `WINNOWER_OPENAI_MODEL`, `WINNOWER_ANTHROPIC_MODEL` - Model overrides
- `WINNOWER_MAX_TOKENS`, `WINNOWER_TEMPERATURE` - Processing parameters
- `WINNOWER_PROMPT_FILE` - Custom prompt file path
- `WINNOWER_PDF_TO_MARKDOWN` - Enable/disable PDF to markdown conversion

## Common Issues and Pitfalls

### API Keys
- **Issue**: Missing API keys cause extraction to fail
- **Solution**: Ensure either `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` is set
- **Check**: Use `--verbose` to see API error details

### PDF Processing
- **Issue**: Some PDFs don't extract text properly (scanned images, complex layouts)
- **Solution**: Default pymupdf4llm conversion handles most cases; PyPDF2 fallback for edge cases
- **Options**: Use `--no-markdown` flag to disable PDF to markdown conversion if needed
- **Fallback**: Tool continues processing but with reduced content quality

### Large Papers
- **Issue**: Papers >100k characters get truncated before AI processing
- **Reason**: API token limits and cost management
- **Behavior**: Content truncated with warning message

### arXiv Rate Limiting
- **Issue**: Processing many arXiv papers quickly may hit rate limits
- **Solution**: Add delays between requests if processing bulk arXiv IDs

### Content Quality
- **Issue**: AI extraction quality varies by paper type and AI model
- **Solution**: Try different models (OpenAI vs Anthropic), adjust temperature, or use domain-specific prompts (ML vs physics)

### Custom Prompts
- **Issue**: Default prompt may not suit specific extraction needs
- **Solution**: Use `--prompt-file` with domain-specific prompts in `winnower/prompts/` or create custom prompts
- **Available**: `ml_focused.txt`, `physics_focused.txt`, `algorithms_focused.txt`, etc.

### PDF to Markdown Benefits
- **Cost Savings**: Markdown format is more token-efficient than raw text extraction
- **Better Structure**: Preserves headings, lists, emphasis, and document hierarchy
- **Improved Extraction**: AI models understand markdown structure better than raw text
- **Formula Handling**: Better preservation of mathematical equations and formulas
- **Quality**: pymupdf4llm specifically designed for academic papers and LLM workflows

## Testing and Development

**Install for Development**:
```bash
uv pip install -e .[dev,test]
```

**Testing Commands**:
```bash
# Run all tests
make test
# OR
python run_tests.py

# Run specific test types
make test-smoke      # Basic functionality tests
make test-unit       # Unit tests only
make test-integration # End-to-end tests

# With coverage
python run_tests.py --coverage
```

**Code Quality Commands**:
```bash
make format    # Format with black
make lint      # Run flake8 and mypy

# Manual commands
black winnower/ tests/
flake8 winnower/ tests/
mypy winnower/
```

**Test Infrastructure**:
- **Smoke tests**: Basic functionality, CLI commands, imports
- **Unit tests**: Individual components (config, parsers, CLI)
- **Integration tests**: End-to-end workflows with mocked APIs
- **Fixtures**: Sample ML and physics papers for testing
- **CI/CD**: GitHub Actions workflow for multi-Python testing

## File Patterns and Conventions

**Supported Input Formats**:
- PDF files: `.pdf` (via PyPDF2)
- Text files: `.txt`, `.md` 
- URLs: Any HTTP/HTTPS URL (auto-detects PDF vs HTML)
- arXiv IDs: Format `YYMM.NNNNN` (e.g., `2501.00089`) or `YYMM.NNNNNvX`
- arXiv URLs: `https://arxiv.org/abs/YYMM.NNNNN` or `/pdf/`
- Directories: Recursive scanning for supported file types

**Output Naming**: `{sanitized_title}_technical_summary.md`

**Code Style**: 
- Black formatting (88 char line length)
- Type hints where applicable
- Docstrings for public methods

## Project History

**Initial Development Requirements**:
- Extract core technical details from papers
- Support files, URLs, arXiv IDs as input
- Python CLI tool targeting technical users
- Filter out benchmarks and promotional content
- Generate markdown summaries

**Key Design Decisions**:
- Modular architecture for easy extension
- Support both OpenAI and Anthropic APIs
- Comprehensive configuration system with multiple input methods
- Configurable extraction prompts for different domains/use cases
- Focus on technical content extraction over general summarization
- Command-line first approach for automation/scripting
- Robust testing infrastructure for CI/CD reliability
- API key management with security best practices

## Future Enhancements

**Potential Improvements**:
- Support for additional input formats (Word docs, LaTeX, etc.)
- Better PDF text extraction (OCR integration for scanned papers)
- Web interface or GUI version
- Batch processing optimizations and parallel processing
- Integration with reference managers (Zotero, Mendeley)
- Support for additional AI providers (Claude, Gemini, local models)
- Paper classification and automatic prompt selection
- Database storage for processed papers and search functionality

## Notes

- **Repository**: https://github.com/jwuphysics/winnower
- **Author**: John F. Wu (jwuphysics@gmail.com)
- **License**: MIT
- **Python Version**: 3.8+

**Important**: Never commit API keys or configuration files with secrets. The `.gitignore` excludes `.env` and `config.json` files for this reason.

## Developer Memories

- Always use the project API keys in .env when testing