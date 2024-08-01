from .constants.route_decorator_constant import ROUTER

def route(method: str, path: str):
    def decorator(func):
        if not hasattr(func, '_routes'):
            func._routes = []
        
        func._routes.append((method, path))
        
        return func
    return decorator

def register_routes(controller_instance):
    router = ROUTER

    for attr_name in dir(controller_instance):
        attr = getattr(controller_instance, attr_name)
        
        if hasattr(attr, '_routes'):
            for method, path in attr._routes:
                router_method = getattr(ROUTER, method)
                router_method(path)(attr)
    
    return router
