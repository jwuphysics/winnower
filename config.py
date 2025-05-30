"""Configuration management for The Winnower."""

import json
import os
from pathlib import Path
from typing import Dict, Optional

from dotenv import load_dotenv


DEFAULT_CONFIG = {
    'openai_model': 'gpt-4',
    'anthropic_model': 'claude-3-sonnet-20240229',
    'max_tokens': 4000,
    'temperature': 0.1,
    'verbose': False,
}


def load_config(config_path: Optional[Path] = None) -> Dict:
    """Load configuration from file and environment."""
    load_dotenv()
    
    config = DEFAULT_CONFIG.copy()
    
    if config_path and config_path.exists():
        with open(config_path, 'r') as f:
            file_config = json.load(f)
            config.update(file_config)
    else:
        default_config_path = Path.home() / '.winnower' / 'config.json'
        if default_config_path.exists():
            with open(default_config_path, 'r') as f:
                file_config = json.load(f)
                config.update(file_config)
    
    env_overrides = {
        'openai_model': os.getenv('WINNOWER_OPENAI_MODEL'),
        'anthropic_model': os.getenv('WINNOWER_ANTHROPIC_MODEL'),
        'max_tokens': os.getenv('WINNOWER_MAX_TOKENS'),
        'temperature': os.getenv('WINNOWER_TEMPERATURE'),
    }
    
    for key, value in env_overrides.items():
        if value is not None:
            if key in ['max_tokens']:
                config[key] = int(value)
            elif key in ['temperature']:
                config[key] = float(value)
            else:
                config[key] = value
    
    return config


def create_default_config(config_dir: Path = None) -> Path:
    """Create default configuration file."""
    if config_dir is None:
        config_dir = Path.home() / '.winnower'
    
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / 'config.json'
    
    with open(config_path, 'w') as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    
    return config_path