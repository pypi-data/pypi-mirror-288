from datetime import datetime
import inspect
from typing import Callable, Optional
from fastapi import FastAPI
from modules.app.app_module import AppModule
import uvicorn
from modulare.factories.application_factory import ApplicationFactory
from modulare.logger import console
from modulare.http.http_server import start_http_server


    
def start():
    app = ApplicationFactory.create(AppModule)

    start_http_server(app, 8000, callback= (
        console.success("Server started")
    ))

start()