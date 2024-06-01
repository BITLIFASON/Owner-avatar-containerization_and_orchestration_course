"""FastAPI application module."""

import os

import uvicorn
from fastapi import FastAPI

import routers
import crud


app = FastAPI(
    title="API online book library",
    description="Homework for the ITMO course",
    contact={"name": "BITLIFASON", "url": "https://github.com/BITLIFASON"},
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

app.include_router(routers.router)

if __name__ == "__main__":

    crud.create_db()

    host = "0.0.0.0"
    port = 80
    uvicorn.run(app, host=host, port=port)
