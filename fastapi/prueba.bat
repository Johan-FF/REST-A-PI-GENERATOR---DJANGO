@echo off
setlocal enabledelayedexpansion

REM Nombre del proyecto y del módulo
set PROJECT_NAME=TIENDA

REM Crear directorio del proyecto
echo Creando directorio del proyecto...
mkdir %PROJECT_NAME%
cd %PROJECT_NAME%

REM Crear un entorno virtual
echo Creando entorno virtual...
python -m venv venv

REM Activar el entorno virtual
echo Activando entorno virtual...
call venv\Scripts\activate

REM Instalar FastAPI y SQLAlchemy
echo Instalando FastAPI y SQLAlchemy...
pip install fastapi sqlalchemy

REM Crear estructura de directorios y archivos
echo Creando estructura de directorios y archivos...
mkdir config
type nul > config\__init__.py
mkdir models
type nul > models\__init__.py
mkdir routes
type nul > routes\__init__.py
mkdir schemas
type nul > schemas\__init__.py

REM Crear archivo app.py
type nul > app.py
echo from fastapi import FastAPI, APIRouter >> app.py
echo app = FastAPI() >> app.py
echo router = APIRouter() >> app.py
echo @router.get("/") >> app.py
echo def read_root(): >> app.py
echo.    return {"message": "Hello World"} >> app.py

REM Ejecutar servidor
call uvicorn app:app --reload
