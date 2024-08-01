from modules.app.app_service import AppService
from modulare.decorators.http import register_routes, route

class AppController:
    def __init__(self, app_service: AppService):
        self.app_service = app_service
        self.router = register_routes(self)

    @route('get', '/')
    def health_check(self):
        return self.app_service.health_check()
