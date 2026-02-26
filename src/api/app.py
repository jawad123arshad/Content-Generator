from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uvicorn
import asyncio
from datetime import datetime
import yaml

from ..models.content_generator import ContentGenerator
from ..monitoring.metrics import MetricsCollector
from ..monitoring.logger import AppLogger

# Load config
with open("./config/config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Initialize app
app = FastAPI(
    title="MLOps Content Generator",
    description=" content generater with MLOps practices",
    version="1.0.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
logger = AppLogger(__name__).get_logger()
metrics = MetricsCollector()
generator = ContentGenerator()

# Request/Response Models
class GenerationRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500)
    max_words: int = Field(50, ge=1, le=500)
    num_lines: int = Field(1, ge=1, le=20)
    temperature: float = Field(0.7, ge=0.1, le=1.0)
    track_metrics: bool = True

class GenerationResponse(BaseModel):
    generation_id: str
    prompt: str
    generated_content: str
    metadata: Dict[str, Any]
    status: str

class BatchGenerationRequest(BaseModel):
    prompts: List[str]
    max_words: int = 50
    num_lines: int = 1
    temperature: float = 0.7

class HealthResponse(BaseModel):
    status: str
    model: str
    device: str
    timestamp: str
    metrics: Optional[Dict[str, Any]] = None

# API Endpoints
@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("Starting up Content Generator API")
    generator.initialize()
    logger.info(f"API initialized with model: {generator.get_model_info()['model_name']}")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down Content Generator API")
    generator.model_loader.unload_model()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MLOps Content Generator API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/generate", response_model=GenerationResponse)
async def generate_content(request: GenerationRequest):
    """Generate content based on prompt"""
    try:
        result = generator.generate(
            prompt=request.prompt,
            max_words=request.max_words,
            num_lines=request.num_lines,
            temperature=request.temperature,
            track_metrics=request.track_metrics
        )
        
        if result["status"] == "failed":
            raise HTTPException(status_code=500, detail=result.get("error", "Generation failed"))
        
        return GenerationResponse(**result)
        
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/batch-generate")
async def batch_generate(request: BatchGenerationRequest):
    """Generate content for multiple prompts"""
    try:
        results = generator.batch_generate(
            prompts=request.prompts,
            max_words=request.max_words,
            num_lines=request.num_lines,
            temperature=request.temperature
        )
        
        return {
            "batch_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "total_prompts": len(request.prompts),
            "successful": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] == "failed"),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Batch generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    model_info = generator.get_model_info()
    
    # Record system metrics
    metrics.record_system_metrics()
    
    return HealthResponse(
        status="healthy",
        model=model_info["model_name"],
        device=model_info["device"],
        timestamp=datetime.now().isoformat(),
        metrics={
            "total_generations": metrics.generation_counter._value.get(),
            "active_model": model_info["model_name"]
        }
    )

@app.get("/metrics")
async def get_metrics():
    """Prometheus metrics endpoint"""
    return Response(content=metrics.get_metrics(), media_type="text/plain")

@app.get("/model/info")
async def model_info():
    """Get current model information"""
    return generator.get_model_info()

@app.post("/model/reload")
async def reload_model(model_name: Optional[str] = None):
    """Reload model (useful for A/B testing)"""
    try:
        generator.model_loader.unload_model()
        if model_name:
            generator.initialize(model_name)
        else:
            generator.initialize()
        
        return {
            "status": "success",
            "message": f"Model reloaded: {generator.get_model_info()['model_name']}"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=config['api']['host'],
        port=config['api']['port'],
        workers=config['api']['workers'],
        reload=True if config['app']['environment'] == "development" else False
    )