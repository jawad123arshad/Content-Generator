from pydantic import BaseModel, validator
from typing import Optional
import re

class GenerationInput(BaseModel):
    prompt: str
    max_words: Optional[int] = 50
    num_lines: Optional[int] = 1
    temperature: Optional[float] = 0.7
    
    @validator('prompt')
    def validate_prompt(cls, v):
        if len(v) < 3:
            raise ValueError('Prompt must be at least 3 characters')
        if len(v) > 1000:
            raise ValueError('Prompt too long (max 1000 chars)')
        return v
    
    @validator('max_words')
    def validate_max_words(cls, v):
        if v < 1 or v > 1000:
            raise ValueError('max_words must be between 1 and 1000')
        return v
    
    @validator('temperature')
    def validate_temperature(cls, v):
        if v < 0.1 or v > 1.0:
            raise ValueError('temperature must be between 0.1 and 1.0')
        return v

class DataValidator:
    """Input validation for the application"""
    
    def validate_input(self, prompt: str, max_words: int, 
                      num_lines: int, temperature: float):
        """Validate all input parameters"""
        
        # Use Pydantic for validation
        GenerationInput(
            prompt=prompt,
            max_words=max_words,
            num_lines=num_lines,
            temperature=temperature
        )
        
        return True