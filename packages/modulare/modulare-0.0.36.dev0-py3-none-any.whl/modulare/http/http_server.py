from typing import Callable, Optional
from fastapi import FastAPI
import uvicorn

def start_http_server(app: FastAPI, port: int = 3000, callback: Optional[Callable] = None):
    if callback: 
        callback()
    uvicorn.run(app, host="0.0.0.0", port=port)