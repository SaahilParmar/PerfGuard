
import sys
import os
import pytest

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config_loader import load_config

def test_load_config_success():
    config = load_config("config/config.yaml")
    assert isinstance(config, dict)
    assert "host" in config
    assert "endpoints" in config

def test_load_config_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_config("config/nonexistent.yaml")
