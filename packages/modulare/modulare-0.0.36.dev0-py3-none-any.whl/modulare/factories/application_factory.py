from fastapi import FastAPI
from infraestructure.containers import AppContainer

class ApplicationFactory:
    resolved_providers = {}
    resolved_controllers = []
             
    def __init__(self, instance):
        self._instance = instance
        self.container = AppContainer()
        self.app = FastAPI()
        self._register_modules()
        self._register_controllers()

    def _register_modules(self):
        modules = getattr(self._instance, 'imports', [])
        for module in modules:
            module_instance = module()
            self._register_controllers_from_module(module_instance)

    def _register_controllers_from_module(self, module_instance):
        controllers = getattr(module_instance, 'controllers', [])
        
        for controller_class in controllers:
            self._register_routes(controller_class)

    def _resolve_and_register_provider(self, provider_class):
        provider_name = provider_class.__name__.lower()
        
        if provider_name in self.resolved_providers:
            return self.resolved_providers[provider_name]

        dependencies = self._resolve_dependencies(provider_class)
        provider_instance = provider_class(**dependencies)
        self.resolved_providers[provider_name] = provider_instance
        
        setattr(self.container, provider_name, provider_instance)
        
        return provider_instance

    def _resolve_dependencies(self, cls):
        parameters = getattr(cls.__init__, '__annotations__', {})
        dependencies = {}
        
        for name, dependency in parameters.items():
            provider_name = dependency.__name__.lower()
            if provider_name in self.resolved_providers:
                dependencies[name] = self.resolved_providers[provider_name]
            else:
                dependencies[name] = self._resolve_and_register_provider(dependency)
        return dependencies

    def _register_controllers(self):
        controllers = self._instance.controllers
        
        for controller_class in controllers:
            self._register_routes(controller_class)

    def _register_routes(self, controller_class):
        dependencies = self._resolve_dependencies(controller_class)
        controller_instance = controller_class(**dependencies)
        self.resolved_controllers.append(controller_instance)
        
        if hasattr(controller_instance, 'router'):
            self.app.include_router(controller_instance.router)

    @classmethod
    def create(cls, module_class):
        return cls(module_class).app
