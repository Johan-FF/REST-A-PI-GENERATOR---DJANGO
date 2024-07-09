@echo off
rem Nombre del proyecto y del módulo
rem Crear directorio del proyecto
echo Crear directorio del proyecto
set "PROJECT_NAME=TIENDA"
mkdir %PROJECT_NAME%
cd %PROJECT_NAME%
rem Crear un entorno virtual
echo Creando entorno virtual...
python -m venv venv


rem Activar el entorno virtual
echo Activando entorno virtual...
call venv/Scripts/activate.bat


rem Instalar FastAPI y Uvicorn
echo Instalando FastAPI y SQLAlchemy...
pip install fastapi
pip install sqlalchemy


rem Crear estructura de directorios y archivos
echo Creando estructura de directorios y archivos...
mkdir config
type NUL > config/__init__.py
mkdir models
type NUL > models/__init__.py
mkdir routes
type NUL > routes/__init__.py
mkdir schemes
type NUL > schemes/__init__.py


rem Crear configuracion DB
echo Crear configuracion DB
type NUL > config/db.py
(
echo from sqlalchemy import create_engine
echo from sqlalchemy.ext.declarative import declarative_base
echo from sqlalchemy.orm import sessionmaker
echo.
echo SQLALCHEMY_DATABASE_URL = ^"sqlite:///./test.db^"
echo.
echo engine = create_engine^(SQLALCHEMY_DATABASE_URL, connect_args={^"check_same_thread^": False}^)
echo SessionLocal = sessionmaker^(autocommit=False, autoflush=False, bind=engine^)
echo Base = declarative_base^(^)
) > config/db.py


rem Crear .gitignore
echo Crear .gitignore
type NUL > .gitignore
(
echo __pycache__/
echo venv/
) > .gitignore


rem Crear README
echo Crear README
type NUL > README.md
(
echo # TIENDA
echo.
echo This is a Python project built with FastAPI that provides basic CRUD operations ^(Create, Read, Update, Delete^) for managing entities, along with authentication using JWT tokens.
echo.
echo ## Requirements
echo.
echo - Python 3.10+
echo - FastAPI
echo - SQLAlchemy
echo - PyJWT
echo.
echo ## Installation
echo.
echo 1. Clone the repository:
echo.
echo ~~~
echo git clone https://github.com/[YOUR-USERNAME]/[YOUR-REPOSIROTY].git
echo cd [YOUR-REPOSIROTY]
echo ~~~
echo.
echo 2. Create a virtual environment ^(optional but recommended^):
echo.
echo ~~~
echo python -m venv venv
echo source venv/bin/activate  # On Windows, use ^'venv\Scripts\activate^'
echo ~~~
echo.
echo 3. Install the dependencies:
echo.
echo ~~~
echo pip install -r requirements.txt
echo ~~~
echo.
echo ## Configuration
echo.
echo Before running the application, make sure to configure the database connection in [YOUR-REPOSIROTY]/config/db.py and configure the CORS in [YOUR-REPOSIROTY]/app.py:
echo.
echo ~~~
echo     allow_origins=[^"https://example.com^", ^"https://anotherdomain.com^"],
echo ~~~
echo.
echo ## Usage
echo.
echo Run the FastAPI application with:
echo.
echo ~~~
echo uvicorn app:app --port 4321 --reload
echo ~~~
echo.
echo This will start the development server, and you can access the API documentation ^(Swagger^) at http://localhost:4321/docs.
echo.
echo ## Contributing
echo.
echo Contributions are welcome! If you find any bugs or want to add new features, feel free to open an issue or submit a pull request.
echo.
) > README.md


rem Crear modelo y esquema
type NUL > models/cliente.py
rem Implementar modelo
echo Implementar modelo Clientes
(
echo from sqlalchemy import Column, String, Integer, ForeignKey
echo from config.db import Base
echo from sqlalchemy.orm import relationship
echo.
echo class Clientes^(Base^):
echo     __tablename__ = ^"Clientes^"
echo.
echo     id_cliente = Column^(Integer, primary_key=True, index=True^)
echo     name = Column^(String, index=True^)
echo     id_factura = Column^(Integer, ForeignKey^(^'Facturas.id_factura^'^)^)
echo     factura = relationship^(^"Facturas^", back_populates=^"clientes^"^)
) > models/cliente.py


type NUL > schemes/cliente.py
rem Implementar esquema
echo Implementar esquema Clientes
(
echo from typing import Optional
echo from pydantic import BaseModel
echo.
echo class Cliente^(BaseModel^):
echo     id_cliente: Optional[int]
echo     name: str
) > schemes/cliente.py


rem # Crear rutas
type NUL > routes/cliente.py
(
echo from fastapi import APIRouter, Depends, HTTPException
echo from sqlalchemy.orm import Session
echo.
echo from models.cliente import Clientes
echo from schemes.cliente import Cliente
echo.
echo from config.db import SessionLocal
echo.
echo cliente = APIRouter^(^)
echo.
echo def get_db^(^):
echo     db = SessionLocal^(^)
echo     try:
echo         yield db
echo     finally:
echo         db.close^(^)
echo.
echo @cliente.post^(^"/^", response_model=Cliente, description=^"Create a new cliente^"^)
echo def create_cliente^(cliente: Cliente, db: Session = Depends^(get_db^)^):
echo     db_item = Clientes^(id_cliente=cliente.id_cliente, name=cliente.name^)
echo     db.add^(db_item^)
echo     db.commit^(^)
echo     db.refresh^(db_item^)
echo     return db_item
echo.
echo @cliente.get^(^"/all^", response_model=list[Cliente], description=^"Get a list of all clientes^"^)
echo def read_clientes^(skip: int = 0, limit: int = 10, db: Session = Depends^(get_db^)^):
echo     return db.query^(Clientes^).offset^(skip^).limit^(limit^).all^(^)
echo.
echo @cliente.get^(^"/{id}^", response_model=Cliente, description=^"Get a single cliente by Id^"^)
echo def read_cliente^(id: int, db: Session = Depends^(get_db^)^):
echo     db_item = db.query^(Clientes^).filter^(Clientes.ID_CLIENTE == id^).first^(^)
echo     if db_item is None:
echo         raise HTTPException^(status_code=404, detail=^"Item not found^"^)
echo     return db_item
echo.
echo @cliente.put^(^"/update/{id}^", response_model=Cliente, description=^"Update a cliente by Id^"^)
echo def update_cliente^(id: int, cliente: Cliente, db: Session = Depends^(get_db^)^):
echo     db_item = db.query^(Clientes^).filter^(Clientes.ID_CLIENTE == id^).first^(^)
echo     if db_item:
echo         db_item.id_cliente = cliente.id_cliente
echo         db_item.name = cliente.name
echo         db.commit^(^)
echo         db.refresh^(db_item^)
echo     if db_item is None:
echo         raise HTTPException^(status_code=404, detail=^"Item not found^"^)
echo     return db_item
echo.
echo @cliente.delete^(^"/delete/{id}^", response_model=Cliente, description=^"Delete a cliente by Id^"^)
echo def delete_cliente^(id: int, db: Session = Depends^(get_db^)^):
echo     db_item = db.query^(Clientes^).filter^(Clientes.ID_CLIENTE == id^).first^(^)
echo     if db_item:
echo         db.delete^(db_item^)
echo         db.commit^(^)
echo     if db_item is None:
echo         raise HTTPException^(status_code=404, detail=^"Item not found^"^)
echo     return db_item
) > routes/cliente.py


rem Crear modelo y esquema
type NUL > models/factura.py
rem Implementar modelo
echo Implementar modelo Facturas
(
echo from sqlalchemy import Column, String, Integer, ForeignKey
echo from config.db import Base
echo from sqlalchemy.orm import relationship
echo.
echo class Facturas^(Base^):
echo     __tablename__ = ^"Facturas^"
echo.
echo     id_factura = Column^(Integer, primary_key=True, index=True^)
echo     fecha = Column^(String, index=True^)
echo     id_cliente = Column^(Integer, ForeignKey^(^'Clientes.id_cliente^'^)^)
echo     cliente = relationship^(^"Clientes^", back_populates=^"facturas^"^)
) > models/factura.py


type NUL > schemes/factura.py
rem Implementar esquema
echo Implementar esquema Facturas
(
echo from typing import Optional
echo from pydantic import BaseModel
echo.
echo class Factura^(BaseModel^):
echo     id_factura: Optional[int]
echo     fecha: str
) > schemes/factura.py


rem # Crear rutas
type NUL > routes/factura.py
(
echo from fastapi import APIRouter, Depends, HTTPException
echo from sqlalchemy.orm import Session
echo.
echo from models.factura import Facturas
echo from schemes.factura import Factura
echo.
echo from config.db import SessionLocal
echo.
echo factura = APIRouter^(^)
echo.
echo def get_db^(^):
echo     db = SessionLocal^(^)
echo     try:
echo         yield db
echo     finally:
echo         db.close^(^)
echo.
echo @factura.post^(^"/^", response_model=Factura, description=^"Create a new factura^"^)
echo def create_factura^(factura: Factura, db: Session = Depends^(get_db^)^):
echo     db_item = Facturas^(id_factura=factura.id_factura, fecha=factura.fecha^)
echo     db.add^(db_item^)
echo     db.commit^(^)
echo     db.refresh^(db_item^)
echo     return db_item
echo.
echo @factura.get^(^"/all^", response_model=list[Factura], description=^"Get a list of all facturas^"^)
echo def read_facturas^(skip: int = 0, limit: int = 10, db: Session = Depends^(get_db^)^):
echo     return db.query^(Facturas^).offset^(skip^).limit^(limit^).all^(^)
echo.
echo @factura.get^(^"/{id}^", response_model=Factura, description=^"Get a single factura by Id^"^)
echo def read_factura^(id: int, db: Session = Depends^(get_db^)^):
echo     db_item = db.query^(Facturas^).filter^(Facturas.ID_FACTURA == id^).first^(^)
echo     if db_item is None:
echo         raise HTTPException^(status_code=404, detail=^"Item not found^"^)
echo     return db_item
echo.
echo @factura.put^(^"/update/{id}^", response_model=Factura, description=^"Update a factura by Id^"^)
echo def update_factura^(id: int, factura: Factura, db: Session = Depends^(get_db^)^):
echo     db_item = db.query^(Facturas^).filter^(Facturas.ID_FACTURA == id^).first^(^)
echo     if db_item:
echo         db_item.id_factura = factura.id_factura
echo         db_item.fecha = factura.fecha
echo         db.commit^(^)
echo         db.refresh^(db_item^)
echo     if db_item is None:
echo         raise HTTPException^(status_code=404, detail=^"Item not found^"^)
echo     return db_item
echo.
echo @factura.delete^(^"/delete/{id}^", response_model=Factura, description=^"Delete a factura by Id^"^)
echo def delete_factura^(id: int, db: Session = Depends^(get_db^)^):
echo     db_item = db.query^(Facturas^).filter^(Facturas.ID_FACTURA == id^).first^(^)
echo     if db_item:
echo         db.delete^(db_item^)
echo         db.commit^(^)
echo     if db_item is None:
echo         raise HTTPException^(status_code=404, detail=^"Item not found^"^)
echo     return db_item
) > routes/factura.py


rem Implementar app.py
echo Implementar app.py
(
echo from fastapi import FastAPI
echo from fastapi.middleware.cors import CORSMiddleware
echo from routes.cliente import cliente
echo from routes.factura import factura
echo from config.db import Base, engine
echo.
echo Base.metadata.create_all^(bind=engine^)
echo.
echo app = FastAPI^(
echo     title=^"TIENDA^",
echo     description=^"REST API using Python, SQLAlchemy and SQLite^",
echo     version=^"0.0.1^",
echo     openapi_tags=[
echo         {
echo             ^"name^": ^"Clientes^",
echo             ^"description^": ^"Clientes endpoint^"
echo         },
echo         {
echo             ^"name^": ^"Facturas^",
echo             ^"description^": ^"Facturas endpoint^"
echo         },
echo     ]
echo ^)
echo.
echo app.add_middleware^(
echo     CORSMiddleware,
echo     allow_origins=[^"*^"],
echo     allow_credentials=True,
echo     allow_methods=[^"*^"],
echo     allow_headers=[^"*^"],
echo ^)
echo.
echo app.include_router^(cliente, prefix=^"/clientes^", tags=[^"Clientes^"]^)
echo app.include_router^(factura, prefix=^"/facturas^", tags=[^"Facturas^"]^)
) > app.py


rem Crear requirements.txt
echo Crear requirements.txt
pip freeze > requirements.txt


rem Ejecutando servidor
echo Ejecutando servidor
uvicorn app:app --port 4321 --reload

