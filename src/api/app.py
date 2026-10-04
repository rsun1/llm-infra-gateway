from fastapi import FastAPI, Request
from uuid import uuid4 
from contextlib import asynccontextmanager
from src.config import settings
#from deployment.manager import ModelDeploymentManager
from src.api.routes import register_routes
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start LLM Router Platform")
    
    yield
    
    print("Shutting down....")

def create_app() -> FastAPI:
    app = FastAPI(title="LLM Router Inference Platform", lifespan=lifespan)
    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid4()))
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:8501",
            "http://127.0.0.1:8501",
        ],
        allow_methods=["GET","POST"],
        allow_headers=["*"]
    )
    register_routes(app)
    return app