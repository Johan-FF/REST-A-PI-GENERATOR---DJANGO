@echo off
rem Nombre del proyecto
rem Crear directorio del proyecto
echo Crear directorio del proyecto
set "PROJECT_NAME=TIENDA"
mkdir %PROJECT_NAME%
cd %PROJECT_NAME%
nest new TIENDA