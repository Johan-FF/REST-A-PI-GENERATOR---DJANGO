from .builder import Builder
from script_builder.concrete_script import ConcreteScript

class FastAPIBuilder(Builder):
    PROJECT_NAME: str = ""
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    def __init__(self, psm_model) -> None:
        """
        A fresh builder instance should contain a blank script object, which is
        used in further assembly.
        """
        self.reset(psm_model.get("project").get("name"))

    def reset(self, project_name: str) -> None:
        FastAPIBuilder.PROJECT_NAME = project_name
        self._script = ConcreteScript()
        
        self._script.add("#!/bin/bash")
        self._script.add("# Nombre del proyecto y del módulo")
        self._script.add(f'PROJECT_NAME="{project_name}"')
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
        
        self._script.add("# Ejecutar servidor")
        self._script.add("uvicorn app:app --reload")
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
        self.reset(FastAPIBuilder.PROJECT_NAME)
        return script

    def produce_crud(self, entity_name: str) -> None:
        pass

    def produce_create(self) -> None:
        pass

    def produce_read(self) -> None:
        pass

    def produce_update(self) -> None:
        pass

    def produce_delete(self) -> None:
        pass