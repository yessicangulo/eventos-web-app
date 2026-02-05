"""
Excepciones personalizadas para la aplicación
"""


class APIException(Exception):
    """Excepción base para errores de la API"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundError(APIException):
    """Recurso no encontrado"""

    def __init__(self, message: str = "Recurso no encontrado"):
        super().__init__(message, status_code=404)


class PermissionError(APIException):
    """Error de permisos"""

    def __init__(self, message: str = "No tienes permisos para realizar esta acción"):
        super().__init__(message, status_code=403)


class ValidationError(APIException):
    """Error de validación"""

    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class ConflictError(APIException):
    """Conflicto (ej: registro duplicado)"""

    def __init__(self, message: str):
        super().__init__(message, status_code=409)
