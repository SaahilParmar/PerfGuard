import yaml
import os

def load_config(config_path="config/config.yaml"):
    """
    Load configuration from the YAML file.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
