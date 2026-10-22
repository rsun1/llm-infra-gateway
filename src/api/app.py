from fastapi import FastAPI, Request
from uuid import uuid4 
from contextlib import asynccontextmanager, suppress
from src.config import settings
#from deployment.manager import ModelDeploymentManager
from src.api.routes import register_routes
from fastapi.middleware.cors import CORSMiddleware
from src.core.serving.backend_adapter import BackendAdapter
from src.core.serving.mock_engine import MockEngine
from src.core.serving.batch_scheduler import BatchScheduler
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Start LLM Router Platform")
    adapter = BackendAdapter()
    adapter.register_engine("mock-7b", MockEngine())
    await adapter.initialize()
    app.state.adapter = adapter
    scheduler = BatchScheduler(
        adapter = adapter,
        max_batch_size = 3,
        max_wait_ms = 300
    )
    app.state.scheduler = scheduler
    watcher_task = asyncio.create_task(scheduler._timeout_watcher())
    try:
        yield
    finally:
        watcher_task.cancel()
        with suppress(asyncio.CancelledError):
            await watcher_task
        await adapter.shutdown()
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