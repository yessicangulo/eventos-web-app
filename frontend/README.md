# Frontend - Sistema de Gestión de Eventos

Frontend React para la gestión de eventos, desarrollado con Vite, React Router y Context API.

## 🚀 Inicio Rápido

### Requisitos Previos

- Node.js 18+ (recomendado 20+)
- npm o yarn
- Backend corriendo en `http://localhost:5000` (o `http://127.0.0.1:5000`)

### Instalación

```bash
# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

## 📋 Scripts Disponibles

```bash
npm run dev      # Servidor de desarrollo (con hot reload)
npm run build    # Construir para producción
npm run preview  # Previsualizar build de producción
npm run lint     # Ejecutar linter
```

## 🏗️ Estructura del Proyecto

```
src/
├── components/          # Componentes reutilizables
│   ├── common/         # Componentes comunes (Button, Input, Card, etc.)
│   ├── events/         # Componentes de eventos (EventCard, EventList, EventForm)
│   └── layout/         # Componentes de layout (Navbar, Layout, PrivateRoute)
├── pages/              # Páginas de la aplicación
│   ├── Home.jsx        # Lista de eventos (página principal)
│   ├── Login.jsx       # Página de login
│   ├── Register.jsx    # Página de registro
│   ├── EventDetail.jsx # Detalle de evento
│   ├── CreateEvent.jsx # Crear evento
│   ├── EditEvent.jsx   # Editar evento
│   └── Profile.jsx     # Perfil de usuario
├── services/           # Servicios de API
│   ├── api.js         # Configuración de Axios
│   ├── authService.js # Servicios de autenticación
│   ├── eventService.js # Servicios de eventos
│   ├── sessionService.js # Servicios de sesiones
│   └── attendeeService.js # Servicios de asistentes
├── context/            # Estado global
│   └── AuthContext.jsx # Context de autenticación
├── utils/              # Utilidades
│   ├── constants.js   # Constantes (roles, estados)
│   └── formatters.js  # Formateo de fechas
├── App.jsx            # Componente principal con rutas
└── main.jsx           # Punto de entrada
```

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

## 🔧 Configuración

### URL del Backend

Por defecto, el frontend se conecta a: `http://127.0.0.1:5000/api/v1`

Para cambiar la URL, crea un archivo `.env` en `frontend/`:

```env
VITE_API_URL=http://localhost:5000/api/v1
```

### Estados de Eventos

Los eventos pueden tener los siguientes estados:

- **SCHEDULED** (Programado): Editable completamente
- **ONGOING** (En Curso): Solo descripción y ubicación editables
- **COMPLETED** (Completado): No editable
- **CANCELLED** (Cancelado): Solo se puede reactivar cambiando el estado

## 🎨 Tecnologías Utilizadas

- **React 18** - Biblioteca de UI
- **Vite** - Herramienta de construcción y desarrollo
- **React Router v6** - Navegación entre páginas
- **Axios** - Cliente HTTP para peticiones al backend
- **Context API** - Estado global (autenticación)

## 📝 Notas Importantes

- El frontend requiere que el backend esté corriendo para funcionar
- Los tokens JWT se guardan en `localStorage`
- Las rutas protegidas redirigen a `/login` si no hay autenticación
- La paginación se muestra automáticamente cuando hay más de 6 eventos


## 📚 Documentación Adicional

- Ver `INICIO_RAPIDO.md` para guía de inicio rápido
- Ver documentación del backend para detalles de la API
