import inspect
from datetime import datetime

class __LoggerService:
    appName = "Modulare"
    colors = {
        "error": "\u001b[31m",
        "info": "\u001b[34m",
        "reset": "\u001b[0m",
        "success": "\u001b[32m",
        "warning": "\u001b[33m",
        "debug": "\u001b[35m"
    }

    def __init__(self, appName=None):
        if appName:
            self.appName = appName

    def __getCurrentTimestamp(self):
        now = datetime.now()

        # Formatar a data e hora no formato desejado
        formatted_date_time = now.strftime("%m/%d/%Y, %I:%M:%S %p")

        return formatted_date_time
    

    def __print(self, color, message):
        print(
            f"{color}[{self.appName}] - "
            f"{self.colors['reset']}{self.__getCurrentTimestamp()} "
            f"{color}{message}{self.colors['reset']}"
        )
       
    def ___print(self, color, *args):
        # Get the caller's local variables
        frame = inspect.currentframe().f_back
        local_vars = frame.f_locals
        # Replace the variables in the message
        message = " ".join(map(str, args)).format(**local_vars)

        self.__print(self.colors[color], message)


    def error(self, *args):
        self.___print('error', *args)

    def info(self, *args):
        self.___print('info', *args)

    def log(self, *args):
        self.___print('reset', *args)

    def success(self, *args):
        self.___print('success', *args)


    def warning(self, *args):
        self.___print('warning', *args)

    def debug(self, *args):
        self.___print('debug', *args)
        
console = __LoggerService("MyApp2")
