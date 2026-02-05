"""
Validadores reutilizables para schemas Pydantic
"""


def validate_page(v: int) -> int:
    """
    Valida que page sea >= 1

    Usage:
        @field_validator('page')
        @classmethod
        def validate_page_field(cls, v):
            return validate_page(v)
    """
    if v < 1:
        raise ValueError("page debe ser mayor o igual a 1")
    return v


def validate_per_page(v: int, max_per_page: int = 100) -> int:
    """
    Valida que per_page sea > 0 y <= max_per_page

    Args:
        v: Valor a validar
        max_per_page: Máximo permitido (default: 100)

    Usage:
        @field_validator('per_page')
        @classmethod
        def validate_per_page_field(cls, v):
            return validate_per_page(v)
    """
    if v <= 0:
        raise ValueError("per_page debe ser mayor a 0")
    if v > max_per_page:
        raise ValueError(f"per_page no puede ser mayor a {max_per_page}")
    return v


def validate_search(v: str | None) -> str | None:
    """
    Valida que search no esté vacío si se proporciona.
    Retorna el string sin espacios al inicio/final.

    Usage:
        @field_validator('search')
        @classmethod
        def validate_search_field(cls, v):
            return validate_search(v)
    """
    if v is not None and len(v.strip()) == 0:
        raise ValueError("search no puede estar vacío")
    return v.strip() if v else None
