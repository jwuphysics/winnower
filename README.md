# The Winnower

Extract core technical details from research papers, with specialized support for ML/statistics and physics/astronomy domains.

## Features

- **Multiple input formats**: Local files, URLs, arXiv IDs, directories
- **Smart PDF processing**: Converts PDFs to markdown for better structure preservation and lower API costs
- **AI-powered extraction**: Uses OpenAI or Anthropic models to identify technical content
- **Focused output**: Extracts methods, algorithms, and implementations
- **Configurable**: Command-line interface with extensive configuration options

## Installation

```bash
pip install -e .
```

## Quick Start

1. Set up The Winnower:
```bash
# Run setup to create configuration files
winnower setup

# Add your API key to ~/.winnower/.env
# OR set environment variable directly:
export OPENAI_API_KEY="your-api-key"
# OR
export ANTHROPIC_API_KEY="your-api-key"
```

2. Process a paper:
```bash
# From arXiv ID
winnower 2501.00089

# From URL
winnower https://arxiv.org/abs/2501.00089

# From local file
winnower paper.pdf

# Process directory recursively
winnower /path/to/papers/ --recursive
```

## Usage

```
winnower [-h] [-o OUTPUT] [-r] [--config CONFIG] [--model {openai,anthropic}] 
         [--prompt-file PROMPT_FILE] [--verbose] [--version] [input]

Extract core technical details from research papers

positional arguments:
  input                 Paper input: file path, directory, URL, or arXiv ID

options:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: current directory)
  -r, --recursive       Process directory recursively
  --config CONFIG       Configuration file path
  --model {openai,anthropic}
                        AI model provider (default: openai)
  --prompt-file PROMPT_FILE
                        Custom extraction prompt file
  --verbose, -v         Enable verbose output
  --version             show program version number and exit

Examples:
  winnower setup                              # Set up configuration
  winnower paper.pdf
  winnower https://arxiv.org/abs/2501.00089
  winnower 2501.00089
  winnower /path/to/papers/ --recursive
```

## Configuration

The Winnower supports multiple ways to configure API keys and settings:

### API Keys (choose one approach):

1. **Global .env file** (recommended for personal use):
```bash
winnower setup  # Creates ~/.winnower/.env template
# Edit ~/.winnower/.env and add your API key
```

2. **Project .env file** (for project-specific keys):
```bash
cp .env.example .env
# Edit .env and add your API key
```

3. **Environment variables** (for CI/CD, Docker):
```bash
export OPENAI_API_KEY="your-key"
# or
export ANTHROPIC_API_KEY="your-key"
```

### Other Settings

Create `~/.winnower/config.json` for non-sensitive settings:

```json
{
  "openai_model": "gpt-4.1-mini-2025-04-14",
  "anthropic_model": "claude-3-sonnet-20240229",
  "max_tokens": 4000,
  "temperature": 0.1,
  "prompt_file": "/path/to/custom_prompt.txt",
  "pdf_to_markdown": true
}
```

Or use environment variables:
- `WINNOWER_OPENAI_MODEL`
- `WINNOWER_ANTHROPIC_MODEL`
- `WINNOWER_MAX_TOKENS`
- `WINNOWER_TEMPERATURE`
- `WINNOWER_PROMPT_FILE`
- `WINNOWER_PDF_TO_MARKDOWN` (true/false)

## Output

The Winnower generates markdown files optimized for two primary domains:

**For ML/Statistics/Applied Math papers:**
- **Core Algorithms**: Step-by-step procedures and computational methods
- **Mathematical Formulations**: Key equations and theoretical foundations
- **Model Architectures**: Technical methods and novel approaches
- **Key Parameters**: Important hyperparameters and configurations

**For Physics/Astronomy papers:**
- **Mathematical Formulations**: Fundamental equations and relationships
- **Conceptual Methods**: Theoretical frameworks and physical principles
- **Physical Models**: Mathematical descriptions of systems and phenomena
- **Characteristic Parameters**: Physical constants and scaling relationships

## Custom Extraction Prompts

The Winnower supports custom extraction prompts for different use cases:

- **Default**: Balanced extraction supporting both ML and physics domains
- **ML-focused**: Emphasizes algorithms, model architectures, and training procedures
- **Physics-focused**: Emphasizes mathematical formulations and conceptual frameworks
- **Algorithm-focused**: Deep focus on algorithmic details and complexity analysis
- **Implementation-focused**: Focuses on architecture and deployment details  
- **Methods summary**: High-level methodological overview

Use `--prompt-file` to specify a custom prompt, or set `prompt_file` in your config. Prompt files should include `{title}` and `{content}` placeholders.

## Examples

```bash
# Process single arXiv paper
winnower 2501.00089 -o summaries/

# Process all PDFs in directory
winnower papers/ --recursive --model anthropic

# Custom config and verbose output
winnower paper.pdf --config my-config.json --verbose

# Use domain-specific extraction prompts
winnower ml_paper.pdf --prompt-file prompts/ml_focused.txt
winnower physics_paper.pdf --prompt-file prompts/physics_focused.txt

# Disable PDF to markdown conversion (legacy mode)
winnower paper.pdf --no-markdown
```

## Requirements

- Python 3.8+
- OpenAI API key OR Anthropic API key
- Internet connection for URL/arXiv processing

## Development

To contribute to The Winnower:

```bash
# Clone and setup
git clone https://github.com/jwuphysics/winnower.git
cd winnower
uv venv && source .venv/bin/activate
uv pip install -e .[dev,test]

# Run tests
make test           # All tests
make test-smoke     # Quick functionality check
make test-unit      # Unit tests only

# Code quality
make format         # Format with black
make lint          # Run flake8 and mypy

# Create .env with test keys for development
cp .env.example .env
# Edit .env with your API keys
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Run tests and ensure they pass (`make test`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

MIT