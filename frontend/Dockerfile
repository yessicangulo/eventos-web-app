FROM node:20-alpine

WORKDIR /app

# Copiar archivos de dependencias primero (para mejor cache de Docker)
COPY package.json package-lock.json* ./

# Instalar dependencias
RUN npm ci

# Copiar código de la aplicación
COPY . .

# Exponer puerto de Vite
EXPOSE 5173

# Comando para desarrollo (con hot reload)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
