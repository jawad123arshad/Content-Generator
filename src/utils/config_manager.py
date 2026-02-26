"""
Configuration management with validation
"""

import os
import yaml
import json
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

class ConfigManager:
    """Manage application configuration"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        load_dotenv()  # Load environment variables
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if not self.config_path.exists():
            # Create default config
            return self._create_default_config()
        
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default configuration"""
        default_config = {
            "app": {
                "name": "MLOps Content Generator",
                "version": "1.0.0",
                "environment": "development"
            },
            "model": {
                "primary_model": "gpt2",
                "fallback_model": "gpt2",
                "cache_dir": "./models/cache",
                "max_length": 500,
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.95
            },
            "api": {
                "host": "0.0.0.0",
                "port": 8000,
                "workers": 1,
                "timeout": 60
            },
            "monitoring": {
                "log_level": "INFO",
                "log_file": "./logs/app.log",
                "metrics_enabled": True,
                "prometheus_port": 9090
            }
        }
        
        # Save default config
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        return default_config
    
    def _validate_config(self):
        """Validate configuration values"""
        required_sections = ["app", "model", "api", "monitoring"]
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required config section: {section}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by dot notation key"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def set(self, key: str, value: Any):
        """Set config value by dot notation key"""
        keys = key.split('.')
        target = self.config
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        target[keys[-1]] = value
        
        # Save to file
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def get_model_config(self, model_name: Optional[str] = None) -> Dict[str, Any]:
        """Get model-specific configuration"""
        model_config = self.config.get("model", {}).copy()
        if model_name:
            model_config["name"] = model_name
        return model_config
    
    def get_api_config(self) -> Dict[str, Any]:
        """Get API configuration"""
        return self.config.get("api", {})
    
    def get_monitoring_config(self) -> Dict[str, Any]:
        """Get monitoring configuration"""
        return self.config.get("monitoring", {})
    
    def is_development(self) -> bool:
        """Check if running in development mode"""
        return self.config["app"]["environment"] == "development"
    
    def is_production(self) -> bool:
        """Check if running in production mode"""
        return self.config["app"]["environment"] == "production"