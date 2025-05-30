# The Winnower

Extract core technical details from research papers.

## Features

- **Multiple input formats**: Local files, URLs, arXiv IDs, directories
- **AI-powered extraction**: Uses OpenAI or Anthropic models to identify technical content
- **Focused output**: Extracts methods, algorithms, and implementations
- **Configurable**: Command-line interface with extensive configuration options

## Installation

```bash
pip install -e .
```

## Quick Start

1. Set up your API key:
```bash
export OPENAI_API_KEY="your-api-key"
# or
export ANTHROPIC_API_KEY="your-api-key"
```

2. Process a paper:
```bash
# From arXiv ID
winnower 2301.00001

# From URL
winnower https://arxiv.org/abs/2301.00001

# From local file
winnower paper.pdf

# Process directory recursively
winnower /path/to/papers/ --recursive
```

## Usage

```
winnower [-h] [-o OUTPUT] [-r] [--config CONFIG] [--model {openai,anthropic}] [--verbose] [--version] input

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
  --verbose, -v         Enable verbose output
  --version             show program version number and exit
```

## Configuration

Create `~/.winnower/config.json`:

```json
{
  "openai_model": "gpt-4",
  "anthropic_model": "claude-3-sonnet-20240229",
  "max_tokens": 4000,
  "temperature": 0.1
}
```

Or use environment variables:
- `WINNOWER_OPENAI_MODEL`
- `WINNOWER_ANTHROPIC_MODEL`
- `WINNOWER_MAX_TOKENS`
- `WINNOWER_TEMPERATURE`

## Output

The Winnower generates markdown files with:

- **Core Methods**: Fundamental approaches and techniques
- **Technical Implementation**: Algorithms, mathematical formulations, architectural details
- **Key Innovations**: Novel technical contributions
- **Technical Parameters**: Important hyperparameters and configurations
- **Experimental Setup**: Technical aspects of experiments (not results)

## Examples

```bash
# Process single arXiv paper
winnower 2301.00001 -o summaries/

# Process all PDFs in directory
winnower papers/ --recursive --model anthropic

# Custom config and verbose output
winnower paper.pdf --config my-config.json --verbose
```

## Requirements

- Python 3.8+
- OpenAI API key OR Anthropic API key
- Internet connection for URL/arXiv processing

## License

MIT