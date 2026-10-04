from fastapi import FastAPI, HTTPException
from src.utils.types import LLMInferRequest


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
    async def list_models():
        return {
            "object": "list",
            "data":[],
        }
        
    @app.post("/v1/chat/completions")
    async def chat_completions(req: LLMInferRequest):
        raise HTTPException(
            status_code=503,
            detail="Inference engine is not initialized yet.",
        )
        
        