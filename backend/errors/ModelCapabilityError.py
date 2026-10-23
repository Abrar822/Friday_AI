from fastapi import HTTPException, status

class ModelCapabilityError(HTTPException):
    def __init__(self):
        message = "The selected model does not support vision capabilities."
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=message)