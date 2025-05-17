import os
import json
from typing import Dict, Any

class ConfigManager:
  
    @staticmethod
    def load_config(config_path: str = None) -> Dict[str, Any]:
       
        # Default config path
        if not config_path:
            config_path = os.path.join(
                os.path.dirname(__file__), 
                '..', '..', 'config', 'login_config.json'
            )
        
        try:
            # Ensure absolute path
            config_path = os.path.abspath(config_path)
            
            # Check file exists
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Configuration file not found: {config_path}")
            
            # Read and parse JSON
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
            
            return config
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise type(e)(f"Error loading configuration: {str(e)}")
    
    @staticmethod
    def get_env_config(key: str, default: Any = None) -> Any:
      
        return os.environ.get(key, default)
    
    @staticmethod
    def save_config(config: Dict[str, Any], config_path: str = None):
       
        if not config_path:
            config_path = os.path.join(
                os.path.dirname(__file__), 
                '..', '..', 'config', 'login_config.json'
            )
        
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
            
            # Write configuration
            with open(config_path, 'w') as config_file:
                json.dump(config, config_file, indent=4)
        except IOError as e:
            raise IOError(f"Error saving configuration: {str(e)}")
