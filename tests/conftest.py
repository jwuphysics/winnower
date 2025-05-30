"""Pytest configuration and shared fixtures."""

import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment with API keys."""
    # Always use test API keys to avoid hitting real APIs during tests
    test_env = {
        'OPENAI_API_KEY': 'test-openai-key',
        'ANTHROPIC_API_KEY': 'test-anthropic-key',
    }
    
    with patch.dict(os.environ, test_env):
        yield


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    
    # Cleanup
    import shutil
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def fixtures_dir():
    """Provide path to test fixtures."""
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_ml_paper(fixtures_dir):
    """Provide sample ML paper content."""
    return fixtures_dir / "sample_ml_paper.txt"


@pytest.fixture
def sample_physics_paper(fixtures_dir):
    """Provide sample physics paper content."""
    return fixtures_dir / "sample_physics_paper.txt"


@pytest.fixture
def mock_openai_response():
    """Provide a mock OpenAI API response."""
    from unittest.mock import Mock
    
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = """
    **Core Algorithms**: Test algorithm extraction
    **Mathematical Formulations**: Test equation: E = mc²
    **Technical Methods**: Test method description
    **Key Parameters**: Test parameters
    """
    return mock_response


@pytest.fixture
def mock_anthropic_response():
    """Provide a mock Anthropic API response."""
    from unittest.mock import Mock
    
    mock_response = Mock()
    mock_response.content = [Mock()]
    mock_response.content[0].text = """
    **Mathematical Formulations**: Test physics equations
    **Conceptual Methods**: Test theoretical framework
    **Physical Models**: Test model description
    **Key Parameters**: Test physics constants
    """
    return mock_response