"""
Utilidades para paginación de consultas
"""

from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Query


def get_pagination_metadata(query: Query, page: int = 1, per_page: int = 100) -> dict[str, Any]:
    """
    Obtiene metadata de paginación de una consulta.

    Esta función maneja correctamente el conteo de consultas agrupadas usando
    un enfoque de subquery, necesario cuando se usa GROUP BY.

    Args:
        query: Objeto Query de SQLAlchemy (puede incluir GROUP BY)
        page: Número de página (1-indexed)
        per_page: Número de items por página

    Returns:
        Diccionario con metadata de paginación:
        - page: Página actual
        - per_page: Items por página
        - total_count: Total de items
        - total_pages: Total de páginas
        - has_next: Si hay página siguiente
        - has_prev: Si hay página anterior
    """
    subquery = query.subquery()
    total_count = query.session.query(func.count()).select_from(subquery).scalar() or 0
    total_pages = (total_count + per_page - 1) // per_page if total_count > 0 else 1
    has_next = page < total_pages
    has_prev = page > 1

    return {
        "page": page,
        "per_page": per_page,
        "total_count": total_count,
        "total_pages": total_pages,
        "has_next": has_next,
        "has_prev": has_prev,
    }


def apply_pagination(query: Query, page: int = 1, per_page: int = 100) -> Query:
    """
    Aplica paginación a una consulta.

    Args:
        query: Objeto Query de SQLAlchemy
        page: Número de página (1-indexed)
        per_page: Número de items por página

    Returns:
        Query con paginación aplicada
    """
    offset = (page - 1) * per_page
    return query.offset(offset).limit(per_page)
