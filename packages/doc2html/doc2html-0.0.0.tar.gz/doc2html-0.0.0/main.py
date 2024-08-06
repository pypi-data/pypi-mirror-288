import os
import uvicorn
from fastapi import FastAPI, UploadFile

from doc2html import config as cfg, schemas, server, reformat


app = FastAPI()


@app.on_event("startup")
async def startup_event() -> None:
    """Setup operations"""
    # Using this instead of lifespan due to library errors when using asynccontextmanager
    cfg.logger.info("Unoserver is starting...")
    await server.handle_start_unoserver()
    cfg.logger.info("Unoserver is active")


@app.on_event("shutdown")
async def shutdown_event() -> None:
    """Shutdown operations"""
    cfg.logger.info("Transformer server is stopping...")


@app.get(
    "/healthcheck",
    status_code=200,
    summary="Verify status of the service",
    response_description="Status and relevant service information (name, version, etc)")
async def get_healthcheck() -> schemas.HealthcheckOutput:
    """
    Status response endpoint as well as info about the service name and version

    Request example:
        ```
        curl --location --request GET 'http://localhost:2024/healthcheck'
        ```
    """
    # Use default values of the healthcheck so that they are only defined in a single point.
    return schemas.HealthcheckOutput()


@app.post(
    "/transform-document",
    status_code=200,
    summary="Transform the format of documents. Typically from doc",
    response_description="Successful operation"
)
async def transform_document(file: UploadFile, to: str = "htm") -> schemas.TransformOutput:
    return await reformat.to_format(file, to)


def start_server() -> None:
    """Launch the server"""
    cfg.logger.info("Starting app...")
    uvicorn.run(app, host=cfg.TRANSFORM_HOST, port=cfg.TRANSFORM_PORT)


if __name__ == "__main__":
    start_server()
