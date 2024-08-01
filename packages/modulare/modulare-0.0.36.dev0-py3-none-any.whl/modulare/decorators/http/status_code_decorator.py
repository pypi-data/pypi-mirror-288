import inspect
from functools import wraps
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel
from .enums.status_code_decorator_enum import StatusCode

def response_status_code(status_code: StatusCode):
    code = status_code.value

    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            response = await func(*args, **kwargs)
            if isinstance(response, Response):
                response.status_code = code
            elif isinstance(response, BaseModel):
                response = JSONResponse(content=response.dict(), status_code=code)
            elif isinstance(response, dict):
                response = JSONResponse(content=response, status_code=code)
            else:
                response = JSONResponse(content={"detail": str(response)}, status_code=code)
            return response

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if isinstance(response, Response):
                response.status_code = code
            elif isinstance(response, BaseModel):
                response = JSONResponse(content=response.dict(), status_code=code)
            elif isinstance(response, dict):
                response = JSONResponse(content=response, status_code=code)
            else:
                response = JSONResponse(content={"detail": str(response)}, status_code=code)
            return response

        if inspect.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
