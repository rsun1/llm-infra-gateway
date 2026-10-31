from fastapi import FastAPI, HTTPException, Request
from src.utils.types import LLMInferRequest
from time import time
from fastapi.responses import StreamingResponse
import json 

def register_routes(app: FastAPI):
    @app.get("/health")
    def health():
        return {"status": "healthy"}
    
    @app.get("/health/live")
    def health_live():
        return {"status":"live"}
    
    @app.get("/health/ready")
    def health_ready():
        return {"status":"ready"}
    
    
    @app.get("/v1/models")
    async def list_models(request: Request):
        registry = request.app.state.registry
        data = []
        for model_name in registry.versions:
            version = registry.get_latest(model_name)
            data.append({
                "id":model_name,
                "version":version.version,
                "stage": version.stage
            })
        return {
            "object": "list",
            "data":data,
        }
        
    @app.post("/v1/chat/completions")
    async def chat_completions(req: LLMInferRequest, request: Request):
        scheduler = request.app.state.scheduler
        metrics = request.app.state.metrics
        start = time()
        try:
            response = await scheduler.submit(req)
        except ValueError as e:
            raise HTTPException(
                status_code=404,
                detail=str(e),
            )
        latency_ms = (time() - start)*1000
        metrics.record_request(req.model,latency_ms)
        return response
    
    @app.get("/metrics")
    async def get_metrics(request: Request):
        registry = request.app.state.registry
        metrics = request.app.state.metrics
        result = {}
        for model_name in registry.versions:
            result[model_name] = {
                "request_count": metrics.get_request_count(model_name),
                "avg_latency_ms": metrics.get_avg_latency(model_name),
                "p95_latency_ms": metrics.get_p95_latency(model_name),
            }
        return result
    
    @app.post("/v1/completions/stream")
    async def completions_stream(req: LLMInferRequest, request: Request):
        adapter = request.app.state.adapter
        
        async def event_generator():
            async for chunk in adapter.generate_stream(req):
                yield f"data: {json.dumps(chunk.model_dump())}\n\n"
            yield "data: [DONE]\n\n"
            
        return StreamingResponse(event_generator(), media_type="text/event-stream")