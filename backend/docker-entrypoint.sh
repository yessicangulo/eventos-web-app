#!/bin/bash
set -e

echo "🚀 Iniciando backend..."

# Esperar a que PostgreSQL esté listo
echo "⏳ Esperando a que PostgreSQL esté disponible..."
until pg_isready -h db -p 5432 -U ${POSTGRES_USER:-postgres} > /dev/null 2>&1; do
  echo "PostgreSQL no está listo aún, esperando..."
  sleep 2
done

echo "✅ PostgreSQL está disponible"

# Crear extensión unaccent para búsquedas sin acentos
echo "🔧 Creando extensión unaccent..."
PGPASSWORD=${POSTGRES_PASSWORD:-postgres} psql -h db -U ${POSTGRES_USER:-postgres} -d ${POSTGRES_DB:-mis_eventos} -c "CREATE EXTENSION IF NOT EXISTS unaccent;" || echo "⚠️  Advertencia: Error al crear extensión unaccent (puede ser normal si ya existe)"

# Ejecutar migraciones
echo "📦 Ejecutando migraciones de base de datos..."
alembic upgrade head || echo "⚠️  Advertencia: Error al ejecutar migraciones (puede ser normal si la DB ya está actualizada)"

# Crear usuarios iniciales (admin y organizador)
echo "👥 Creando usuarios iniciales..."
python -m app.scripts.create_admin || echo "⚠️  Advertencia: Error al crear usuarios iniciales (puede ser normal si ya existen)"

# Ejecutar el comando pasado como argumento
echo "🎯 Iniciando aplicación..."
exec "$@"
