import typer 
import uvicorn
from src.api.app import create_app 

cli = typer.Typer(name="LLM Infra CLI")

@cli.command("serve-api")
def serve_api(host: str = "127.0.0.1",port:int=8000):
    app = create_app()
    uvicorn.run(app,host=host,port=port)
    
if __name__ == "__main__":
    cli()