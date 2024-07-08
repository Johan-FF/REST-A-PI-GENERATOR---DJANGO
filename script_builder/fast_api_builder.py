from .builder import Builder
from script_builder.concrete_script import ConcreteScript
from .utils.data_types import types_to_valid_sqlalchemy_types, \
                            remove_special_characters_and_capitalize, \
                            type_to_valid_sqlalchemy_type

class FastAPIBuilder(Builder):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    PROJECT_NAME: str = ""
    VERSION: str = ""
    EXECUTE_PORT: str = ""
    OPERATING_SYSTEM: str = ""

    def __init__(self, psm_model) -> None:
        """
        A fresh builder instance should contain a blank script object, which is
        used in further assembly.
        """
        FastAPIBuilder.OPERATING_SYSTEM = psm_model.find("so").get("so-name")

        project_name = psm_model.find("project").get("name")
        FastAPIBuilder.PROJECT_NAME = project_name

        technology = psm_model.find("technology")
        FastAPIBuilder.EXECUTE_PORT = technology.get("port")
        FastAPIBuilder.VERSION = technology.get("version")

        self.reset()

    def reset(self) -> None:
        self._script = ConcreteScript()
        
        self._script.add("#!/bin/bash")
        self._script.add("# Nombre del proyecto y del módulo")
        self._script.add(f'PROJECT_NAME="{FastAPIBuilder.PROJECT_NAME}"')
        self._script.add("\n")

        self._script.add("# Crear directorio del proyecto")
        self._script.add('echo "Creando directorio del proyecto..."')
        self._script.add("mkdir $PROJECT_NAME")
        self._script.add("cd $PROJECT_NAME")
        self._script.add("\n")
        
        self._script.add("# Crear un entorno virtual")
        self._script.add('echo "Creando entorno virtual..."')
        self._script.add("python -m venv venv")
        self._script.add("\n")
        
        self._script.add("# Activar el entorno virtual")
        self._script.add('echo "Activando entorno virtual..."')
        self._script.add("venv/Scripts/activate")
        self._script.add("\n")
        
        self._script.add("# Instalar FastAPI y Uvicorn")
        self._script.add('echo "Instalando FastAPI y SQLAlchemy..."')
        self._script.add("pip install fastapi")
        self._script.add("pip install sqlalchemy")
        self._script.add("\n")
        
        self._script.add("# Crear estructura de directorios y archivos")
        self._script.add('echo "Creando estructura de directorios y archivos..."')
        self._script.add("mkdir config")
        self._script.add("touch config/__init__.py")
        self._script.add("mkdir models")
        self._script.add("touch models/__init__.py")
        self._script.add("mkdir routes")
        self._script.add("touch routes/__init__.py")
        self._script.add("mkdir schemes")
        self._script.add("touch schemes/__init__.py")
        self._script.add("\n")

        self._script.add("# Crear configuracion DB")
        self._script.add('echo "Crear configuracion DB"')
        self._script.add("touch config/db.py")
        self._script.add("cat <<EOT > config/db.py")
        self._script.add("from sqlalchemy import create_engine")
        self._script.add("from sqlalchemy.ext.declarative import declarative_base")
        self._script.add('from sqlalchemy.orm import sessionmaker')
        self._script.add("\n")
        self._script.add('SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"')
        self._script.add("\n")
        self._script.add('engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})')
        self._script.add('SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)')
        self._script.add('Base = declarative_base()')
        self._script.add("EOT")
        self._script.add("\n")

        self._script.add("# Crear .gitignore")
        self._script.add('echo "Crear .gitignore"')
        self._script.add("touch .gitignore")
        self._script.add("cat <<EOT > .gitignore")
        self._script.add("__pycache__/")
        self._script.add("venv/")
        self._script.add("EOT")
        self._script.add("\n")

        self._script.add("# Crear README")
        self._script.add('echo "Crear README"')
        self._script.add("touch README.md")
        self._script.add("cat <<EOT > README.md")
        self._script.add(f"# {FastAPIBuilder.PROJECT_NAME}")
        self._script.add("\n")
        self._script.add("This is a Python project built with FastAPI that provides basic CRUD operations (Create, Read, Update, Delete) for managing entities, along with authentication using JWT tokens.")
        self._script.add("\n")
        self._script.add("## Requirements")
        self._script.add("\n")
        self._script.add("- Python 3.10+")
        self._script.add("- FastAPI")
        self._script.add("- SQLAlchemy")
        self._script.add("- PyJWT")
        self._script.add("\n")
        self._script.add("## Installation")
        self._script.add("\n")
        self._script.add("1. Clone the repository:")
        self._script.add("\n")
        self._script.add("~~~")
        self._script.add("git clone https://github.com/[YOUR-USERNAME]/[YOUR-REPOSIROTY].git")
        self._script.add("cd [YOUR-REPOSIROTY]")
        self._script.add("~~~")
        self._script.add("\n")
        self._script.add("2. Create a virtual environment (optional but recommended):")
        self._script.add("\n")
        self._script.add("~~~")
        self._script.add("python -m venv venv")
        self._script.add("source venv/bin/activate  # On Windows, use `venv\Scripts\activate`")
        self._script.add("~~~")
        self._script.add("\n")
        self._script.add("3. Install the dependencies:")
        self._script.add("\n")
        self._script.add("~~~")
        self._script.add("pip install -r requirements.txt")
        self._script.add("~~~")
        self._script.add("\n")
        self._script.add("## Configuration")
        self._script.add("\n")
        self._script.add("Before running the application, make sure to configure the database connection in [YOUR-REPOSIROTY]/config/db.py and configure the CORS in [YOUR-REPOSIROTY]/app.py:")
        self._script.add("\n")
        self._script.add("~~~")
        self._script.add('    allow_origins=["https://example.com", "https://anotherdomain.com"],')
        self._script.add("~~~")
        self._script.add("\n")
        self._script.add("## Usage")
        self._script.add("\n")
        self._script.add("Run the FastAPI application with:")
        self._script.add("\n")
        self._script.add("~~~")
        self._script.add(f"uvicorn app:app --port {FastAPIBuilder.EXECUTE_PORT} --reload")
        self._script.add("~~~")
        self._script.add("\n")
        self._script.add(f"This will start the development server, and you can access the API documentation (Swagger) at http://localhost:{FastAPIBuilder.EXECUTE_PORT}/docs.")
        self._script.add("\n")
        self._script.add("## Contributing")
        self._script.add("\n")
        self._script.add("Contributions are welcome! If you find any bugs or want to add new features, feel free to open an issue or submit a pull request.")
        self._script.add("\n")
        self._script.add("Before submitting a pull request, please ensure that the tests pass and the code complies with the project's coding standards.")
        self._script.add("EOT")
        self._script.add("\n")

    def produce_app_file(self, entities_name: list[str]) -> None:
        self._script.add("# Implementar app.py")
        self._script.add('echo "Implementar app.py"')
        self._script.add(f"cat <<EOT > app.py")
        self._script.add("from fastapi import FastAPI")
        self._script.add("from fastapi.middleware.cors import CORSMiddleware")
        for entity in entities_name:
            entity_name_lower = entity.lower()
            self._script.add(f"from routes.{entity_name_lower} import {entity_name_lower}")
        self._script.add("from config.db import Base, engine")
        self._script.add("\n")
        self._script.add("Base.metadata.create_all(bind=engine)")
        self._script.add("\n")
        self._script.add("app = FastAPI(")
        self._script.add(f'    title="{FastAPIBuilder.PROJECT_NAME}",')
        self._script.add('    description="REST API using Python, SQLAlchemy and SQLite",')
        self._script.add('    version="0.0.1",')
        self._script.add("    openapi_tags=[")
        for entity in entities_name:
            table_name = remove_special_characters_and_capitalize(entity)+"s"
            self._script.add("        {")
            self._script.add(f'        "name": "{table_name}",')
            self._script.add(f'        "description": "{table_name} endpoint"')
            self._script.add("        },")
        self._script.add("    ]")
        self._script.add(")")
        self._script.add("\n")

        self._script.add("app.add_middleware(")
        self._script.add("    CORSMiddleware,")
        self._script.add("    allow_origins=["*"],")
        self._script.add("    allow_credentials=True,")
        self._script.add("    allow_methods=["*"],")
        self._script.add("    allow_headers=["*"],")
        self._script.add(")")
        self._script.add("\n")

        for entity in entities_name:
            entity_name_lower = entity.lower()
            table_name = remove_special_characters_and_capitalize(entity)+"s"
            self._script.add(f'app.include_router({entity_name_lower}, prefix="/{entity_name_lower}s", tags=["{table_name}"])')
        self._script.add("EOT")
        self._script.add("\n")

        self._script.add("# Crear requirements.txt")
        self._script.add(f"pip freeze > requirements.txt")
        self._script.add("\n")

        self._script.add("# Ejecutar servidor")
        self._script.add(f"uvicorn app:app --port {FastAPIBuilder.EXECUTE_PORT} --reload")
        self._script.add("\n")

    @property
    def script(self) -> ConcreteScript:
        """
        Concrete Builders are supposed to provide their own methods for
        retrieving results. That's because various types of builders may create
        entirely different scripts that don't follow the same interface.
        Therefore, such methods cannot be declared in the base Builder interface
        (at least in a statically typed programming language).

        Usually, after returning the end result to the client, a builder
        instance is expected to be ready to start producing another script.
        That's why it's a usual practice to call the reset method at the end of
        the `getScript` method body. However, this behavior is not mandatory,
        and you can make your builders wait for an explicit reset call from the
        client code before disposing of the previous result.
        """
        script = self._script
        self.reset()
        return script

    def produce_crud(self, entity_name: str, attributes: list[dict], relations: dict[str, str]) -> None:
        entity_name_lower = entity_name.lower()
        self._script.add("# Crear modelo y esquema")
        self._script.add(f"touch models/{entity_name_lower}.py")
        
        table_name = remove_special_characters_and_capitalize(entity_name)+"s"
        self._create_models(entity_name_lower, table_name, relations, attributes)

        self._script.add(f"touch schemes/{entity_name_lower}.py")
        self._create_schemas(entity_name_lower, table_name, attributes)

        self._script.add("# Crear rutas")
        self._script.add(f"touch routes/{entity_name_lower}.py")
        self._script.add(f"cat <<EOT > routes/{entity_name_lower}.py")
        self._script.add("from fastapi import APIRouter, Depends, HTTPException")
        self._script.add("from sqlalchemy.orm import Session")
        self._script.add("\n")
        self._script.add(f"from models.{entity_name_lower} import {table_name}")
        self._script.add(f"from schemes.{entity_name_lower} import {table_name[:-1]}")
        self._script.add("\n")
        self._script.add("from config.db import SessionLocal")
        self._script.add("\n")
        self._script.add(f"{entity_name_lower} = APIRouter()")
        self._script.add("\n")
        self._script.add("def get_db():")
        self._script.add("    db = SessionLocal()")
        self._script.add("    try:")
        self._script.add("        yield db")
        self._script.add("    finally:")
        self._script.add("        db.close()")
        self._script.add("\n")
        
        pk_attribute: str = ""
        for attribute in attributes:
            if attribute.get("is-pk"):
                pk_attribute = attribute.get("name")
        self.produce_create(entity_name_lower, table_name, attributes)
        self.produce_read(entity_name_lower, table_name, pk_attribute)
        self.produce_update(entity_name_lower, table_name, pk_attribute, attributes)
        self.produce_delete(entity_name_lower, table_name, pk_attribute)
        
        self._script.add("EOT")
        self._script.add("\n")

    def _create_models(self, entity_name_lower: str, table_name: str, relations: dict[str, str], attributes: list[dict]) -> None:
        self._script.add("# Implementar modelo")
        self._script.add(f'echo "Implementar modelo {table_name}"')
        self._script.add(f"cat <<EOT > models/{entity_name_lower}.py")
        empty_relations = len(relations)==0
        self._script.add(f"from sqlalchemy import Column, {types_to_valid_sqlalchemy_types(attributes)}{", ForeignKey" if not empty_relations else ""}")
        self._script.add("from config.db import Base")
        if not empty_relations:
            self._script.add("from sqlalchemy.orm import relationship")
        self._script.add("\n")
        self._script.add(f"class {table_name}(Base):")
        self._script.add(f'    __tablename__ = "{table_name}"')
        self._script.add("\n")
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()

            if attribute.get("is-pk"):
                self._script.add(f"    {attribute_name} = Column({type_to_valid_sqlalchemy_type(attribute.get("data-type"))}, primary_key=True, index=True)")
                continue

            self._script.add(f"    {attribute_name} = Column({type_to_valid_sqlalchemy_type(attribute.get("data-type"))}, index=True)")
        for attribute_of_table, table in relations.items():
            fk_attribute = attribute_of_table.lower()
            fk_table_lower = table.lower()
            fk_table_name = remove_special_characters_and_capitalize(table)
            self._script.add(f"    {fk_attribute} = Column(Integer, ForeignKey('{fk_table_name}s.{fk_attribute}'))")
            self._script.add(f'    {fk_table_lower} = relationship("{fk_table_name}s", back_populates="{table_name.lower()}")')
        self._script.add("EOT")
        self._script.add("\n")

    def _create_schemas(self, entity_name_lower: str, table_name: str, attributes: list[dict]) -> None:
        self._script.add("# Implementar esquema")
        self._script.add(f'echo "Implementar esquema {table_name}"')
        self._script.add(f"cat <<EOT > schemes/{entity_name_lower}.py")
        self._script.add("from typing import Optional")
        self._script.add("from pydantic import BaseModel")
        self._script.add("\n")
        self._script.add(f"class {table_name[:-1]}(BaseModel):")
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()

            if attribute.get("is-pk"):
                self._script.add(f"    {attribute_name}: Optional[{attribute.get("data-type").__name__}]")
                continue

            self._script.add(f"    {attribute_name}: {attribute.get("data-type").__name__}")
        self._script.add("EOT")
        self._script.add("\n")

    def produce_create(self, entity_name_lower: str, table_name: str, attributes: list[dict]) -> None:
        self._script.add(f'@{entity_name_lower}.post("/", response_model={table_name[:-1]}, description="Create a new {entity_name_lower}")')
        self._script.add(f"def create_{entity_name_lower}({entity_name_lower}: {table_name[:-1]}, db: Session = Depends(get_db)):")
        create_str = f"    db_item = {table_name}("
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()
            create_str += f"{attribute_name}={entity_name_lower}.{attribute_name}, "
        self._script.add(create_str[:-2]+")")
        self._script.add("    db.add(db_item)")
        self._script.add("    db.commit()")
        self._script.add("    db.refresh(db_item)")
        self._script.add("    return db_item")
        self._script.add("\n")

    def produce_read(self, entity_name_lower: str, table_name: str, pk_attribute: str) -> None:
        self._script.add(f'@{entity_name_lower}.get("/all", response_model=list[{table_name[:-1]}], description="Get a list of all {entity_name_lower}s")')
        self._script.add(f"def read_{entity_name_lower}s(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):")
        self._script.add(f"    return db.query({table_name}).offset(skip).limit(limit).all()")
        self._script.add("\n")
        self._script.add(f'@{entity_name_lower}.get("/{{id}}", response_model={table_name[:-1]}, description="Get a single {entity_name_lower} by Id")')
        self._script.add(f"def read_{entity_name_lower}(id: int, db: Session = Depends(get_db)):")
        self._script.add(f"    db_item = db.query({table_name}).filter({table_name}.{pk_attribute} == id).first()")
        self._script.add("    if db_item is None:")
        self._script.add('        raise HTTPException(status_code=404, detail="Item not found")')
        self._script.add("    return db_item")
        self._script.add("\n")

    def produce_update(self, entity_name_lower: str, table_name: str, pk_attribute: str, attributes: list[dict]) -> None:
        self._script.add(f'@{entity_name_lower}.put("/update/{{id}}", response_model={table_name[:-1]}, description="Update a {entity_name_lower} by Id")')
        self._script.add(f"def update_{entity_name_lower}(id: int, {entity_name_lower}: {table_name[:-1]}, db: Session = Depends(get_db)):")
        self._script.add(f"    db_item = db.query({table_name}).filter({table_name}.{pk_attribute} == id).first()")
        self._script.add("    if db_item:")
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()
            self._script.add(f"        db_item.{attribute_name} = {entity_name_lower}.{attribute_name}")
        self._script.add("        db.commit()")
        self._script.add("        db.refresh(db_item)")
        self._script.add("    if db_item is None:")
        self._script.add('        raise HTTPException(status_code=404, detail="Item not found")')
        self._script.add("    return db_item")
        self._script.add("\n")

    def produce_delete(self, entity_name_lower: str, table_name: str, pk_attribute: str) -> None:
        self._script.add(f'@{entity_name_lower}.delete("/delete/{{id}}", response_model={table_name[:-1]}, description="Delete a {entity_name_lower} by Id")')
        self._script.add(f"def delete_{entity_name_lower}(id: int, db: Session = Depends(get_db)):")
        self._script.add(f"    db_item = db.query({table_name}).filter({table_name}.{pk_attribute} == id).first()")
        self._script.add("    if db_item:")
        self._script.add("        db.delete(db_item)")
        self._script.add("        db.commit()")
        self._script.add("    if db_item is None:")
        self._script.add('        raise HTTPException(status_code=404, detail="Item not found")')
        self._script.add("    return db_item")