from modulare.logger import console

class AppService:
    def health_check(self):
        message = "API is up and running on version 1.0.0"

        console.info(message)

        return message