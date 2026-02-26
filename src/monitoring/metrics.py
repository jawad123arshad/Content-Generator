"""
Metrics collection with singleton pattern to avoid duplicate registration
"""

from prometheus_client import Counter, Histogram, Gauge, generate_latest, CollectorRegistry
import time
from typing import Optional
import psutil
import json
from datetime import datetime
import threading

class MetricsCollector:
    """Singleton metrics collector to avoid duplicate registrations"""
    
    _instance = None
    _lock = threading.Lock()
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        # Create a new registry to avoid conflicts
        self.registry = CollectorRegistry(auto_describe=True)
        
        # Define metrics with the custom registry
        self.generation_counter = Counter(
            'content_generations_total',
            'Total number of content generations',
            ['model_name', 'status'],
            registry=self.registry
        )
        
        self.generation_duration = Histogram(
            'content_generation_duration_seconds',
            'Time spent on generation',
            ['model_name'],
            buckets=(0.1, 0.5, 1.0, 2.0, 5.0, 10.0),
            registry=self.registry
        )
        
        self.prompt_length = Histogram(
            'prompt_length_chars',
            'Length of prompts in characters',
            buckets=(10, 50, 100, 200, 500),
            registry=self.registry
        )
        
        self.generated_length = Histogram(
            'generated_length_chars',
            'Length of generated content in characters',
            buckets=(50, 100, 200, 500, 1000, 2000),
            registry=self.registry
        )
        
        self.model_load_counter = Counter(
            'model_loads_total',
            'Total number of model loads',
            ['model_name', 'success'],
            registry=self.registry
        )
        
        self.model_load_duration = Histogram(
            'model_load_duration_seconds',
            'Time spent loading models',
            ['model_name'],
            registry=self.registry
        )
        
        self.active_model = Gauge(
            'active_model',
            'Currently active model',
            ['model_name'],
            registry=self.registry
        )
        
        self.system_memory = Gauge(
            'system_memory_usage_bytes',
            'System memory usage',
            registry=self.registry
        )
        
        self.system_cpu = Gauge(
            'system_cpu_usage_percent',
            'System CPU usage',
            registry=self.registry
        )
        
        self._initialized = True
    
    def record_generation(self, generation_id: str, prompt_length: int,
                         generated_length: int, generation_time: float,
                         model_name: str, status: str = "success"):
        """Record metrics for a generation"""
        
        self.generation_counter.labels(
            model_name=model_name, status=status
        ).inc()
        
        self.generation_duration.labels(
            model_name=model_name
        ).observe(generation_time)
        
        self.prompt_length.observe(prompt_length)
        self.generated_length.observe(generated_length)
        
        # Also save to local file for analysis
        self._save_metric_to_file({
            "timestamp": datetime.now().isoformat(),
            "type": "generation",
            "generation_id": generation_id,
            "prompt_length": prompt_length,
            "generated_length": generated_length,
            "generation_time": generation_time,
            "model_name": model_name,
            "status": status
        })
        
    def record_model_load(self, model_name: str, load_time: float, success: bool):
        """Record model loading metrics"""
        
        self.model_load_counter.labels(
            model_name=model_name, success=str(success)
        ).inc()
        
        self.model_load_duration.labels(
            model_name=model_name
        ).observe(load_time)
        
        if success:
            self.active_model.labels(model_name=model_name).set(1)
            
    def record_system_metrics(self):
        """Record system resource usage"""
        try:
            self.system_memory.set(psutil.virtual_memory().used)
            self.system_cpu.set(psutil.cpu_percent(interval=1))
        except:
            pass  # Silently fail if psutil fails
            
    def _save_metric_to_file(self, metric: dict):
        """Save metric to file for long-term storage"""
        try:
            with open("./logs/metrics.jsonl", "a") as f:
                f.write(json.dumps(metric) + "\n")
        except:
            pass  # Silently fail if can't write to file
            
    def get_metrics(self):
        """Get all metrics in Prometheus format"""
        return generate_latest(self.registry)