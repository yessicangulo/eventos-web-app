FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Poetry
RUN pip install --no-cache-dir poetry

# Configurar Poetry para no crear virtualenv (ya estamos en un contenedor)
RUN poetry config virtualenvs.create false

# Copiar archivos de dependencias primero (para mejor cache de Docker)
COPY pyproject.toml poetry.lock* ./

# Instalar dependencias (incluyendo dev para tests y herramientas)
RUN poetry install --no-interaction --no-ansi

# Copiar código de la aplicación
COPY . .

# Crear directorio para logs si es necesario
RUN mkdir -p /app/logs

# Exponer puerto
EXPOSE 5000

# Script de inicio - copiar explícitamente y asegurar permisos
# Convertir finales de línea Windows (CRLF) a Unix (LF) si es necesario
RUN if [ -f docker-entrypoint.sh ]; then \
        cp docker-entrypoint.sh /docker-entrypoint.sh && \
        sed -i 's/\r$//' /docker-entrypoint.sh && \
        chmod +x /docker-entrypoint.sh; \
    else \
        echo "ERROR: docker-entrypoint.sh no encontrado" && exit 1; \
    fi

ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["python", "run.py"]
