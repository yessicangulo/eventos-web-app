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

# Verificar si hay migraciones existentes
MIGRATIONS_DIR="alembic/versions"
MIGRATION_COUNT=$(find "$MIGRATIONS_DIR" -name "*.py" -not -name "__init__.py" 2>/dev/null | wc -l || echo "0")

# Si no hay migraciones, generar la inicial automáticamente desde los modelos
if [ "$MIGRATION_COUNT" -eq "0" ]; then
    echo "📝 No se encontraron migraciones. Generando migración inicial desde los modelos..."
    alembic revision --autogenerate -m "Initial migration - create all tables" || {
        echo "⚠️  Error al generar migración automática. Verifica que los modelos estén correctos."
        exit 1
    }
    echo "✅ Migración inicial generada automáticamente"
fi

# Ejecutar migraciones
echo "📦 Ejecutando migraciones de base de datos..."
alembic upgrade head || {
    echo "⚠️  Error al ejecutar migraciones"
    exit 1
}

# Crear usuarios iniciales (admin y organizador)
echo "👥 Creando usuarios iniciales..."
python -m app.scripts.create_admin || echo "⚠️  Advertencia: Error al crear usuarios iniciales (puede ser normal si ya existen)"

# Ejecutar el comando pasado como argumento
echo "🎯 Iniciando aplicación..."
exec "$@"
