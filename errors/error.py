class APIError(Exception):
    pass

class AuthError(APIError):
    code = 403
    description = "Authentication Error"

class AdminError(APIError):
    code = 401
    description = "Administration Error"

class NotFoundError(APIError):
    code = 404
    description = "Not Found Error"

class NotAllowedError(APIError):
    code = 401
    description = "Not Allowed Error"