# Mis Eventos - Sistema de Gestión de Eventos

Aplicación web Full Stack para la gestión eficiente de eventos.

## 🏗️ Estructura del Proyecto

```
.
├── backend/          # API REST con FastAPI
├── frontend/         # Frontend (pendiente)
├── Doc/             # Documentación
└── docker-compose.yml
```

## 🚀 Inicio Rápido

### Backend

Consulta el [README del backend](./backend/README.md) para instrucciones detalladas.

```bash
cd backend
poetry install
poetry shell
python run.py
```

### Docker

```bash
docker-compose up --build
```

## 📋 Requisitos

- Python 3.12+
- PostgreSQL 15+
- Poetry
- Docker y Docker Compose (opcional)

## 🛠️ Tecnologías

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pytest

### Frontend
- Pendiente de implementación

## 📝 Documentación

- [Backend README](./backend/README.md)
- API Documentation: http://localhost:5000/swagger

## 🧪 Testing

```bash
cd backend
poetry run pytest
poetry run pytest --cov=app --cov-report=html
```
