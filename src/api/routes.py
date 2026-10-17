from fastapi import FastAPI, HTTPException, Request
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
    async def chat_completions(req: LLMInferRequest, request: Request):
        adapter = request.app.state.adapter
        try:
            response = await adapter.generate(req)
        except ValueError as e:
            raise HTTPException(
                status_code=404,
                detail=str(e),
            )
        return response
        