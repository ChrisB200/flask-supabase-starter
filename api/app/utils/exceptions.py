class AppError(Exception):
    def __init__(self, message="Something went wrong", status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
