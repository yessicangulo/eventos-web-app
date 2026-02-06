# Mis Eventos - Sistema de Gestión de Eventos

Aplicación web Full Stack para la gestión eficiente de eventos.

## 🏗️ Estructura del Proyecto

```
.
├── backend/          # API REST con FastAPI
├── frontend/         # Frontend React con Vite
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

El backend estará disponible en: **http://localhost:5000**

### Frontend

Consulta el [README del frontend](./frontend/README.md) o [INICIO_RAPIDO.md](./frontend/INICIO_RAPIDO.md) para instrucciones detalladas.

```bash
cd frontend
npm install
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

**Nota**: El frontend requiere que el backend esté corriendo para funcionar correctamente.

### Docker

```bash
docker-compose up --build
```

## 📋 Requisitos

### Backend
- Python 3.12+
- PostgreSQL 15+
- Poetry
- Docker y Docker Compose (opcional)

### Frontend
- Node.js 18+ (recomendado 20+)
- npm o yarn

## 🛠️ Tecnologías

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pytest

### Frontend
- React 18
- Vite
- React Router v6
- Axios
- Context API

## 📝 Documentación

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)
- [Frontend Inicio Rápido](./frontend/INICIO_RAPIDO.md)
- API Documentation: http://localhost:5000/swagger

## 🔑 Funcionalidades Principales

### Autenticación
- Registro de usuarios (rol ATTENDEE por defecto)
- Login con JWT tokens
- Gestión de sesión persistente
- Rutas protegidas según rol

### Gestión de Eventos
- Lista de eventos con paginación y filtros
- Búsqueda por nombre
- Filtros por estado (Programado, En Curso, Completado, Cancelado)
- Detalle de evento con sesiones
- Crear eventos (requiere rol ADMIN o ORGANIZER)
- Editar eventos (con validaciones según estado)
- Eliminar eventos

### Registro a Eventos
- Registrarse a eventos (rol ATTENDEE)
- Cancelar registro
- Ver eventos registrados

### Perfil de Usuario
- Ver información del usuario
- Ver eventos creados (ORGANIZER/ADMIN)
- Ver eventos registrados (ATTENDEE)

## 🧪 Testing

### Backend

```bash
cd backend
poetry run pytest
poetry run pytest --cov=app --cov-report=html
```

### Frontend

```bash
cd frontend
npm run lint
```

## 🔗 URLs Importantes

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api/v1
- **Swagger UI**: http://localhost:5000/swagger
