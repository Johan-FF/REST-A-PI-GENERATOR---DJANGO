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
        self._script.add("mkdir schemas")
        self._script.add("touch schemas/__init__.py")
        self._script.add("\n")
        
        self._script.add("# Crear archivo app.py")
        self._script.add("touch app.py")
        self._script.add("cat <<EOT > app.py")
        self._script.add("from fastapi import FastAPI, APIRouter")
        self._script.add("app = FastAPI()")
        self._script.add('router = APIRouter()')
        self._script.add('@router.get("/")')
        self._script.add("def read_root():")
        self._script.add('    return {"message": "Hello World"}')
        self._script.add("EOT")
        self._script.add("\n")
        
        # self._script.add("# Ejecutar servidor")
        # self._script.add(f"uvicorn app:app --port {FastAPIBuilder.EXECUTE_PORT} --reload")
        # self._script.add("\n")

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

    def produce_crud(self, entity_name: str, attributes: list, relations: dict) -> None:
        entity_name_lower = entity_name.lower()
        self._script.add("# Crear modelo y esquema")
        self._script.add(f"touch models/{entity_name_lower}.py")
        self._script.add(f"touch schemas/{entity_name_lower}.py")
        
        self._script.add("# Implementar modelo")
        self._script.add(f"cat <<EOT > models/{entity_name_lower}.py")
        empty_relations = len(relations)==0
        self._script.add(f"from sqlalchemy import Column, {types_to_valid_sqlalchemy_types(attributes)}{", ForeignKey" if not empty_relations else ""}")
        self._script.add("from config.db import Base")
        if not empty_relations:
            self._script.add("from sqlalchemy.orm import relationship")
        table_name = remove_special_characters_and_capitalize(entity_name)+"s"
        self._script.add(f"class {table_name}(Base):")
        self._script.add(f'    __tablename__ = "{table_name}"')
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()

            if attribute.get("is-pk"):
                self._script.add(f"    {attribute_name} = Column({type_to_valid_sqlalchemy_type(attribute.get("data-type"))}, primary_key=True, index=True)")
                continue

            self._script.add(f"    {attribute_name} = Column({type_to_valid_sqlalchemy_type(attribute.get("data-type"))}, index=True)")
        for attribute_of_table, table in relations.items():
            fk_table_lower = table.lower()
            fk_table_name = remove_special_characters_and_capitalize(table)
            self._script.add(f"    {fk_table_lower}_{attribute_of_table.lower()} = Column(Integer, ForeignKey('{fk_table_name}.{attribute_of_table.lower()}'))")
            self._script.add(f'    {fk_table_lower} = relationship("{fk_table_name}", back_populates="{table_name.lower()}")')
        self._script.add("EOT")
        self._script.add("\n")

        self._script.add("# Implementar esquema")
        self._script.add(f"cat <<EOT > schemas/{entity_name_lower}.py")
        self._script.add("from typing import Optional")
        self._script.add("from pydantic import BaseModel")
        self._script.add(f"class {table_name[:-1]}(BaseModel):")
        for attribute in attributes:
            attribute_name = attribute.get("name").lower()

            if attribute.get("is-pk"):
                self._script.add(f"    {attribute_name}: Optional[{attribute.get("data-type").__name__}]")
                continue

            self._script.add(f"    {attribute_name}: {attribute.get("data-type").__name__}")
        self._script.add("EOT")
        self._script.add("\n")

    def produce_create(self) -> None:
        pass

    def produce_read(self) -> None:
        pass

    def produce_update(self) -> None:
        pass

    def produce_delete(self) -> None:
        pass