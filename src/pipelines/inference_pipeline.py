# """
# Complete inference pipeline with batching, caching, and monitoring
# """

# import asyncio
# from typing import List, Dict, Any, Optional
# from dataclasses import dataclass
# from datetime import datetime
# import hashlib
# import json
# from pathlib import Path
# import aiocache
# from aiocache import cached, Cache

# from ..models.content_generator import ContentGenerator
# from ..monitoring.metrics import MetricsCollector
# from ..monitoring.logger import AppLogger

# @dataclass
# class InferenceRequest:
#     """Inference request data"""
#     prompt: str
#     max_words: int = 50
#     num_lines: int = 1
#     temperature: float = 0.7
#     request_id: Optional[str] = None
    
#     def __post_init__(self):
#         if not self.request_id:
#             self.request_id = hashlib.md5(
#                 f"{self.prompt}_{self.max_words}_{self.num_lines}_{datetime.now()}".encode()
#             ).hexdigest()[:8]

# @dataclass
# class InferenceResponse:
#     """Inference response data"""
#     request_id: str
#     generated_content: str
#     processing_time: float
#     model_name: str
#     timestamp: str
#     cached: bool = False
#     error: Optional[str] = None

# class InferencePipeline:
#     """Production inference pipeline with optimizations"""
    
#     def __init__(self, config_path: str = "config/config.yaml"):
#         self.logger = AppLogger(__name__).get_logger()
#         self.metrics = MetricsCollector()
#         self.generator = ContentGenerator(config_path)
#         self.cache_dir = Path("./cache/inference")
#         self.cache_dir.mkdir(parents=True, exist_ok=True)
        
#         # Initialize generator
#         self.generator.initialize()
        
#     @cached(ttl=3600, cache=Cache.MEMORY)  # 1 hour cache
#     async def generate_async(self, request: InferenceRequest) -> InferenceResponse:
#         """Async generation with caching"""
        
#         self.logger.info(f"Processing request {request.request_id}")
#         start_time = datetime.now()
        
#         try:
#             # Run generation in thread pool
#             loop = asyncio.get_event_loop()
#             result = await loop.run_in_executor(
#                 None,
#                 self.generator.generate,
#                 request.prompt,
#                 request.max_words,
#                 request.num_lines,
#                 request.temperature
#             )
            
#             processing_time = (datetime.now() - start_time).total_seconds()
            
#             response = InferenceResponse(
#                 request_id=request.request_id,
#                 generated_content=result["generated_content"],
#                 processing_time=processing_time,
#                 model_name=self.generator.get_model_info()["model_name"],
#                 timestamp=datetime.now().isoformat()
#             )
            
#             # Cache to disk as well
#             self._cache_to_disk(request.request_id, response)
            
#             return response
            
#         except Exception as e:
#             self.logger.error(f"Error processing request {request.request_id}: {e}")
#             return InferenceResponse(
#                 request_id=request.request_id,
#                 generated_content="",
#                 processing_time=(datetime.now() - start_time).total_seconds(),
#                 model_name="",
#                 timestamp=datetime.now().isoformat(),
#                 error=str(e)
#             )
    
#     async def batch_generate_async(self, requests: List[InferenceRequest], 
#                                   max_concurrent: int = 5) -> List[InferenceResponse]:
#         """Process multiple requests concurrently"""
        
#         # Use semaphore to limit concurrency
#         semaphore = asyncio.Semaphore(max_concurrent)
        
#         async def process_with_limit(request):
#             async with semaphore:
#                 return await self.generate_async(request)
        
#         tasks = [process_with_limit(req) for req in requests]
#         responses = await asyncio.gather(*tasks, return_exceptions=True)
        
#         # Handle exceptions
#         processed_responses = []
#         for i, response in enumerate(responses):
#             if isinstance(response, Exception):
#                 processed_responses.append(InferenceResponse(
#                     request_id=requests[i].request_id,
#                     generated_content="",
#                     processing_time=0,
#                     model_name="",
#                     timestamp=datetime.now().isoformat(),
#                     error=str(response)
#                 ))
#             else:
#                 processed_responses.append(response)
        
#         return processed_responses
    
#     def _cache_to_disk(self, request_id: str, response: InferenceResponse):
#         """Cache response to disk"""
#         cache_file = self.cache_dir / f"{request_id}.json"
#         with open(cache_file, 'w') as f:
#             json.dump({
#                 "request_id": response.request_id,
#                 "generated_content": response.generated_content,
#                 "model_name": response.model_name,
#                 "timestamp": response.timestamp
#             }, f)
    
#     def get_cached_response(self, request_id: str) -> Optional[InferenceResponse]:
#         """Retrieve cached response from disk"""
#         cache_file = self.cache_dir / f"{request_id}.json"
#         if cache_file.exists():
#             with open(cache_file, 'r') as f:
#                 data = json.load(f)
#                 return InferenceResponse(
#                     request_id=data["request_id"],
#                     generated_content=data["generated_content"],
#                     processing_time=0,
#                     model_name=data["model_name"],
#                     timestamp=data["timestamp"],
#                     cached=True
#                 )
#         return None
    
#     def clear_cache(self):
#         """Clear all caches"""
#         # Clear memory cache
#         cache = Cache.MEMORY
#         cache.clear()
        
#         # Clear disk cache
#         for cache_file in self.cache_dir.glob("*.json"):
#             cache_file.unlink()
        
#         self.logger.info("Cache cleared")