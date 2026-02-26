"""
Structured logging for MLOps application
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
import json
from datetime import datetime
import os

class AppLogger:
    """Structured logging for MLOps application"""
    
    def __init__(self, name: str, log_file: str = "./logs/app.log"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        # Create logs directory
        log_dir = Path("./logs")
        log_dir.mkdir(exist_ok=True)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_format)
        
        # File handler with rotation
        try:
            file_handler = RotatingFileHandler(
                log_file, maxBytes=10485760, backupCount=5
            )
            file_handler.setLevel(logging.DEBUG)
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            file_handler.setFormatter(file_format)
            self.logger.addHandler(file_handler)
        except Exception as e:
            print(f"Warning: Could not create file handler: {e}")
        
        self.logger.addHandler(console_handler)
        
    def get_logger(self):
        return self.logger
    
    def log_prediction(self, prediction_data: dict):
        """Log prediction with structured format"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": "INFO",
            "type": "prediction",
            "data": prediction_data
        }
        
        try:
            log_dir = Path("./logs")
            log_dir.mkdir(exist_ok=True)
            
            with open("./logs/predictions.json", "a") as f:
                f.write(json.dumps(log_entry) + "\n")
        except:
            pass  # Silently fail if can't write