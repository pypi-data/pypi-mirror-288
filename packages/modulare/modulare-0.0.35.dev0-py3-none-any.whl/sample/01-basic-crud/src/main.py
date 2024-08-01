from modules.app.app_module import AppModule
from modulare.factories.application_factory import ApplicationFactory
from modulare.logger import console
from modulare.http.http_server import start_http_server

def start():
    app = ApplicationFactory.create(AppModule)

    start_http_server(app)

start()