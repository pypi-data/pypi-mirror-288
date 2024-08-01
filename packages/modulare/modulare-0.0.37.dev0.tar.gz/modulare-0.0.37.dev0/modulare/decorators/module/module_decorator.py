def Module(metadata):
    def decorator(cls):
        cls._module_metadata = metadata
        cls.imports = metadata.get('imports', [])
        cls.controllers = metadata.get('controllers', [])

        return cls
        
    return decorator
