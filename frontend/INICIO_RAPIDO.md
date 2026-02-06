# ⚡ Inicio Rápido - Frontend

## 🚀 Iniciar el Frontend en 3 Pasos

### 1. Instalar Dependencias (solo la primera vez)

```bash
cd frontend
npm install
```

### 2. Verificar que el Backend esté Corriendo

El backend debe estar disponible en: **http://localhost:5000**

Puedes verificar:
- Abre: http://localhost:5000/swagger
- O ejecuta: `curl http://localhost:5000/health`

### 3. Iniciar el Frontend

```bash
npm run dev
```

El frontend estará disponible en: **http://localhost:5173**

---

## 📋 Comandos Disponibles

```bash
# Desarrollo (con hot reload)
npm run dev

# Construir para producción
npm run build

# Previsualizar build de producción
npm run preview

# Linting
npm run lint
```

---

## 🔗 URLs Importantes

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000/api/v1
- **Swagger UI**: http://localhost:5000/swagger

---

## ⚙️ Configuración

El frontend está configurado para conectarse a:
- **URL Base del API**: `http://localhost:5000/api/v1`

Si necesitas cambiar esto, crea un archivo `.env` en `frontend/`:

```env
VITE_API_URL=http://localhost:5000/api/v1
```

---

## 🧪 Probar la Aplicación

1. **Abre**: http://localhost:5173
2. **Regístrate**: Crea una cuenta nueva
3. **Explora**: Navega por los eventos
4. **Crea eventos**: (necesitas rol ORGANIZER)

Para más detalles, consulta: [GUIA_CONEXION_Y_PRUEBA.md](./GUIA_CONEXION_Y_PRUEBA.md)

---

## 🐛 Problemas Comunes

### El frontend no se conecta al backend

1. Verifica que el backend esté corriendo: http://localhost:5000/swagger
2. Revisa la consola del navegador (F12) para ver errores
3. Verifica que `BACKEND_CORS_ORIGINS` en el backend incluya `http://localhost:5173`

### Error 401 Unauthorized

- Cierra sesión y vuelve a iniciar sesión
- O limpia el localStorage: `localStorage.clear()` en la consola del navegador
