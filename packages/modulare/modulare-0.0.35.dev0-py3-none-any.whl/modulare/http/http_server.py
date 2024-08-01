from typing import Callable, Optional
import uvicorn

def start_http_server(self, app, port: int, callback: Optional[Callable] = None):
    if callback: callback()
    uvicorn.run(app, host="0.0.0.0", port=port)