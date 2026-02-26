"""
Complete API tests
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.api.app import app

client = TestClient(app)

class TestAPI:
    """Test all API endpoints"""
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()
        assert "MLOps Content Generator" in response.json()["message"]
    
    def test_health_endpoint(self):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "model" in data
        assert "device" in data
    
    def test_generate_endpoint(self):
        response = client.post(
            "/generate",
            json={
                "prompt": "Write a welcome message",
                "max_words": 20,
                "num_lines": 1,
                "temperature": 0.7
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "generated_content" in data
        assert "generation_id" in data
    
    def test_generate_invalid_input(self):
        response = client.post(
            "/generate",
            json={
                "prompt": "",  # Invalid empty prompt
                "max_words": 20,
                "num_lines": 1,
                "temperature": 0.7
            }
        )
        assert response.status_code == 422  # Validation error
    
    def test_batch_generate(self):
        response = client.post(
            "/batch-generate",
            json={
                "prompts": ["Test 1", "Test 2"],
                "max_words": 10,
                "num_lines": 1,
                "temperature": 0.7
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "batch_id" in data
        assert data["total_prompts"] == 2
    
    def test_model_info(self):
        response = client.get("/model/info")
        assert response.status_code == 200
        data = response.json()
        assert "model_name" in data
        assert "device" in data
    
    def test_metrics_endpoint(self):
        response = client.get("/metrics")
        assert response.status_code == 200
        assert "text/plain" in response.headers["content-type"]