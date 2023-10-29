
from collections.abc import Generator

from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.config import config
from app.exceptions import custom_exception_handler
from app.health import health_api
from app.logging import start_logging, stop_logging


@asynccontextmanager
async def lifespan(_: FastAPI) -> Generator:
    start_logging()
    yield
    stop_logging()


app = FastAPI(
    title=f"{config['NAME']}-service",
    lifespan=lifespan,
)


# Enables CORS for all routes, methods and callers.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Add routers
app.include_router(health_api.router)


# Catch all exceptions
app.exception_handler(Exception)(custom_exception_handler)
