from enum import Enum

class StatusCode(Enum):
    SUCCESS = 200
    CREATED = 201
    BAD_REQUEST = 400
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500