# Guía para Subir a GitHub

## Pasos para subir el proyecto a GitHub

### 1. Crear repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `mis-eventos` (o el nombre que prefieras)
3. Descripción: "Sistema de gestión de eventos - Prueba técnica"
4. **NO** inicialices con README, .gitignore o licencia (ya los tenemos)
5. Haz clic en "Create repository"

### 2. Conectar repositorio local con GitHub

Después de crear el repositorio, GitHub te mostrará comandos. Ejecuta estos comandos:

```bash
# Asegúrate de estar en la raíz del proyecto
cd C:\Users\Dell\OneDrive\Documentos\Datos

# Agrega el remote (reemplaza TU_USUARIO con tu usuario de GitHub)
git remote add origin https://github.com/TU_USUARIO/mis-eventos.git

# O si prefieres SSH:
# git remote add origin git@github.com:TU_USUARIO/mis-eventos.git
```

### 3. Hacer el primer commit

```bash
# Verificar que pre-commit funcione
git commit -m "Initial commit: Backend con FastAPI"

# Si pre-commit encuentra errores, corrígelos y vuelve a hacer commit
```

### 4. Subir a GitHub

```bash
# Cambiar a branch main (si GitHub usa main en lugar de master)
git branch -M main

# Subir el código
git push -u origin main
```

## Verificar pre-commit

Para probar que pre-commit funciona antes de hacer commit:

```bash
cd backend
poetry run pre-commit run --all-files
```

## Comandos útiles

```bash
# Ver estado
git status

# Ver qué archivos están staged
git status --short

# Si quieres saltar pre-commit (no recomendado)
git commit --no-verify -m "mensaje"

# Ver remotes configurados
git remote -v

# Cambiar URL del remote
git remote set-url origin NUEVA_URL
```
