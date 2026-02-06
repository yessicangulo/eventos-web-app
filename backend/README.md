# Mis Eventos - Backend

API REST para gestión de eventos desarrollada con FastAPI.

## Requisitos

- Python 3.12+
- PostgreSQL 15+
- Poetry

## Instalación Local

### 1. Instalar dependencias

```bash
poetry install
```

### 2. Activar el entorno virtual

```bash
poetry shell
```

### 3. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/mis_eventos

# Security
SECRET_KEY=tu-clave-secreta-super-segura-cambia-esto-en-produccion
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]

# App
PROJECT_NAME=Mis Eventos API
VERSION=1.0.0
API_V1_PREFIX=/api/v1
```

### 4. Crear base de datos y ejecutar migraciones

```bash
createdb mis_eventos
alembic upgrade head
```

### 5. Ejecutar servidor

```bash
python run.py
```

La API estará disponible en http://localhost:5000

## Estructura del Proyecto

```
backend/
├── app/
│   ├── __init__.py          # Factory para crear la app FastAPI
│   ├── config.py            # Configuración con Pydantic Settings
│   ├── database.py          # Setup de SQLAlchemy
│   ├── models/              # Modelos SQLAlchemy
│   ├── schemas/             # Schemas Pydantic para validación
│   ├── api/                 # Routers de endpoints (solo llaman a servicios)
│   │   └── v1/              # API v1
│   ├── services/            # Servicios con lógica de negocio
│   ├── crud/                # Operaciones CRUD (capa de acceso a datos)
│   ├── core/                # Utilidades core (seguridad, excepciones)
│   └── tests/               # Tests
├── alembic/                 # Migraciones de base de datos
├── pyproject.toml           # Dependencias con Poetry
└── README.md
```

## Gestión de Usuarios y Roles

### Usuarios Iniciales

Al iniciar con Docker, se crean automáticamente:
- **Administrador**: `admin@mis-eventos.com` / `admin123`
- **Organizador**: `organizer@mis-eventos.com` / `organizer123`

Para crear usuarios manualmente:
```bash
python -m app.scripts.create_admin
```

### Roles Disponibles

- **`admin`**: Acceso completo al sistema
- **`organizer`**: Puede crear y gestionar eventos
- **`attendee`**: Puede registrarse a eventos (rol por defecto en registro público)

## Docker

### Requisitos
- Docker y Docker Compose instalados
- Archivo `.env` configurado en la raíz del proyecto

### Inicio rápido

```bash
# Construir y levantar servicios
docker-compose up --build

# En segundo plano
docker-compose up -d

# Ver logs
docker-compose logs -f backend

# Detener servicios
docker-compose down
```

### Flujo automático

Al ejecutar `docker-compose up`, el sistema automáticamente:
1. Crea la base de datos PostgreSQL
2. Ejecuta migraciones (crea tablas)
3. Crea usuarios iniciales (admin y organizador)
4. Inicia el backend FastAPI

### Servicios disponibles

- **Backend**: http://localhost:5000
- **Swagger UI**: http://localhost:5000/swagger

## Endpoints Principales

### Autenticación

- `POST /api/v1/auth/register` - Registro de usuario (público, siempre crea como `attendee`)
- `POST /api/v1/auth/login` - Login de usuario (público)
- `GET /api/v1/auth/me` - Perfil del usuario actual (requiere autenticación)

### Eventos

- `GET /api/v1/events` - Listar eventos (con búsqueda y filtros)
- `GET /api/v1/events/{id}` - Detalle de evento
- `POST /api/v1/events` - Crear evento (requiere rol ORGANIZER)
- `PUT /api/v1/events/{id}` - Actualizar evento (requiere rol ORGANIZER)
- `DELETE /api/v1/events/{id}` - Eliminar evento (requiere rol ORGANIZER)
- `GET /api/v1/events/my/events` - Mis eventos creados (requiere rol ORGANIZER)

### Sesiones

- `GET /api/v1/sessions/event/{event_id}` - Sesiones de un evento
- `GET /api/v1/sessions/{id}` - Detalle de sesión
- `POST /api/v1/sessions` - Crear sesión (requiere rol ORGANIZER)
- `PUT /api/v1/sessions/{id}` - Actualizar sesión (requiere rol ORGANIZER)
- `DELETE /api/v1/sessions/{id}` - Eliminar sesión (requiere rol ORGANIZER)

### Usuarios (Solo ADMIN)

- `GET /api/v1/users` - Listar usuarios (con filtros y paginación)
- `GET /api/v1/users/{user_id}` - Obtener detalle de usuario
- `POST /api/v1/users` - Crear usuario (organizadores o asistentes)
- `PUT /api/v1/users/{user_id}` - Actualizar usuario (cambiar rol, activar/desactivar)

### Asistentes

- `POST /api/v1/attendees/register/{event_id}` - Registrarse a un evento (requiere rol ATTENDEE)
- `DELETE /api/v1/attendees/unregister/{event_id}` - Cancelar registro (requiere rol ATTENDEE)
- `GET /api/v1/attendees/my-events` - Eventos a los que estoy registrado (requiere rol ATTENDEE)
- `GET /api/v1/attendees/event/{event_id}/attendees` - Lista de asistentes (requiere rol ORGANIZER)
- `GET /api/v1/attendees/check/{event_id}` - Verificar si estoy registrado (requiere rol ATTENDEE)

## Reglas de Negocio

### Eventos
- **Estados**: SCHEDULED (programado), ONGOING (en curso), COMPLETED (completado), CANCELLED (cancelado)
- **Estados automáticos**: ONGOING y COMPLETED se calculan según fechas
- **Edición por estado**:
  - SCHEDULED: Editable (fechas solo si no ha iniciado)
  - ONGOING: Solo descripción y ubicación
  - COMPLETED/CANCELLED: No editable
- **Capacidad**: No puede ser menor que el número de asistentes ya registrados ni menor que la máxima capacidad de sesiones

### Sesiones
- Deben estar dentro del rango de fechas del evento
- La capacidad de la sesión no puede exceder la capacidad del evento
- Pueden ser gestionadas por ORGANIZER o ADMIN

### Asistentes
- No se puede registrar a un evento lleno
- No se puede registrar dos veces al mismo evento
- Solo ATTENDEE puede registrarse

### Usuarios
- Solo ADMIN puede crear usuarios (excepto admin)
- El registro público siempre crea usuarios como ATTENDEE
- Los eventos pueden ser creados/eliminados por ORGANIZER o ADMIN

## Desarrollo

```bash
# Migraciones
alembic revision --autogenerate -m "Descripción del cambio"
alembic upgrade head

# Formatear código
poetry run black app/

# Linting
poetry run flake8 app/

# Testing
poetry run pytest
poetry run pytest --cov=app --cov-report=html
poetry run pytest --cov=app --cov-report=xml  # Para CI/CD
```

**Cobertura mínima requerida:** 50%

**Reportes de cobertura:**
- HTML: `htmlcov/index.html` (abrir en navegador)
- XML: `coverage.xml` (para herramientas CI/CD)
- Terminal: Se muestra al ejecutar los tests

**Nota:** Los directorios `htmlcov/` y archivo `coverage.xml` están en `.gitignore` y no se suben al repositorio.

## Autenticación y Tokens

### Configuración de Tokens

El sistema utiliza autenticación JWT con tokens que expiran después de **24 horas (1 día)** por defecto.

**Decisión de diseño:**
- Para esta versión inicial, se optó por un token de duración extendida (1 día) en lugar de implementar un sistema de refresh tokens.
- Esta decisión prioriza la simplicidad y la experiencia de usuario durante el desarrollo y pruebas iniciales.
- Un token de 1 día permite que los usuarios trabajen durante una jornada completa sin interrupciones por expiración.
- La implementación de refresh tokens se considera una mejora futura para cuando el proyecto requiera mayor seguridad o control de sesiones.

**Configuración:**
- El tiempo de expiración se configura mediante la variable de entorno `ACCESS_TOKEN_EXPIRE_MINUTES` (valor por defecto: 1440 minutos = 24 horas).
- Para cambiar la duración, modifica esta variable en el archivo `.env`.

**Nota:** En un entorno de producción, se recomienda considerar la implementación de refresh tokens para mayor seguridad y control de sesiones.

## Notas

- Autenticación JWT: `Authorization: Bearer <token>`
- Rutas protegidas: `Depends(get_current_user)` o `Depends(require_roles(...))`
