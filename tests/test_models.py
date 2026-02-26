"""
Complete test suite for models module
"""

import pytest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.models.content_generator import ContentGenerator
from src.models.model_loader import ModelLoader
from src.models.model_registry import ModelRegistry
from src.utils.data_validator import DataValidator, GenerationInput
from pydantic import ValidationError

class TestModelLoader:
    """Test model loading functionality"""
    
    def test_initialization(self):
        loader = ModelLoader("config/config.yaml")
        assert loader is not None
        assert loader.device in ["cuda", "cpu"]
    
    def test_model_load(self):
        loader = ModelLoader("config/config.yaml")
        result = loader.load_model("gpt2", fallback=False)
        assert result["status"] == "success"
        assert result["model_name"] == "gpt2"
        assert "model" in result
    
    def test_model_load_fallback(self):
        loader = ModelLoader("config/config.yaml")
        result = loader.load_model("nonexistent-model", fallback=True)
        assert result["status"] == "success"
        assert result["model_name"] == "gpt2"  # Should fallback to gpt2
    
    def test_unload_model(self):
        loader = ModelLoader("config/config.yaml")
        loader.load_model("gpt2")
        assert loader.current_model is not None
        loader.unload_model()
        assert loader.current_model is None

class TestModelRegistry:
    """Test model registry functionality"""
    
    def test_registry_initialization(self):
        registry = ModelRegistry("./test_registry")
        assert registry.registry is not None
        assert "models" in registry.registry
    
    def test_register_model(self):
        registry = ModelRegistry("./test_registry")
        model_id = registry.register_model(
            model_name="gpt2",
            model_version="1.0.0",
            model_path="test/path",
            metrics={"accuracy": 0.95},
            tags={"test": "true"}
        )
        assert model_id is not None
        assert len(model_id) > 0
    
    def test_get_model(self):
        registry = ModelRegistry("./test_registry")
        registry.register_model("gpt2", "1.0.0", "path", {"test": 1})
        model = registry.get_model("gpt2")
        assert model is not None
        assert model["model_name"] == "gpt2"
    
    def test_deactivate_model(self):
        registry = ModelRegistry("./test_registry")
        model_id = registry.register_model("gpt2", "1.0.0", "path", {"test": 1})
        result = registry.deactivate_model(model_id)
        assert result is True
        
        # Check it's deactivated
        model = registry.get_model("gpt2")
        assert model["status"] == "inactive"

class TestContentGenerator:
    """Test main content generator"""
    
    @pytest.fixture
    def generator(self):
        gen = ContentGenerator("config/config.yaml")
        gen.initialize("gpt2")
        return gen
    
    def test_generation_basic(self, generator):
        result = generator.generate(
            prompt="Hello, world",
            max_words=10,
            num_lines=1,
            temperature=0.5
        )
        assert result["status"] == "success"
        assert "generated_content" in result
        assert "generation_id" in result
        assert len(result["generated_content"]) > 0
    
    def test_generation_with_lines(self, generator):
        result = generator.generate(
            prompt="Write a story",
            max_words=20,
            num_lines=3,
            temperature=0.7
        )
        assert result["status"] == "success"
        # Check if we have approximately 3 lines
        lines = result["generated_content"].split('\n\n')
        assert len(lines) <= 4  # Could be 3 with proper formatting
    
    def test_generation_invalid_input(self, generator):
        with pytest.raises(ValidationError):
            result = generator.generate(
                prompt="",  # Empty prompt should fail validation
                max_words=10,
                num_lines=1,
                temperature=0.5
            )
    
    def test_batch_generation(self, generator):
        prompts = ["Test 1", "Test 2", "Test 3"]
        results = generator.batch_generate(prompts, max_words=10)
        assert len(results) == 3
        assert all(r["status"] == "success" for r in results)

class TestDataValidator:
    """Test input validation"""
    
    def test_valid_input(self):
        validator = DataValidator()
        result = validator.validate_input("Valid prompt", 50, 1, 0.7)
        assert result is True
    
    def test_invalid_prompt_length(self):
        validator = DataValidator()
        with pytest.raises(ValidationError):
            validator.validate_input("a", 50, 1, 0.7)  # Too short
    
    def test_invalid_temperature(self):
        validator = DataValidator()
        with pytest.raises(ValidationError):
            validator.validate_input("Valid", 50, 1, 2.0)  # Too high
    
    def test_pydantic_model(self):
        # Test GenerationInput directly
        valid = GenerationInput(prompt="Test", max_words=50, num_lines=1, temperature=0.7)
        assert valid.prompt == "Test"
        
        with pytest.raises(ValidationError):
            GenerationInput(prompt="", max_words=50, num_lines=1, temperature=0.7)

# Run tests with: pytest tests/test_models.py -v