from .create_script import CreateScript
from ..concrete_script import ConcreteScript

class LinuxCreator(CreateScript):
    """
    Concrete classes have to implement all abstract operations of the base
    class. They can also override some operations with a default implementation.
    """

    def __init__(self) -> None:
        super().__init__()
        self._script.add("#!/bin/bash")

    def add_comment(self, comment: str) -> None:
        self._script.add("# "+comment)
    
    def add_print(self, msg: str) -> None:
        self._script.add(f'echo "{msg}"')

    def add_enter_project_packague(self, project_anme: str) -> None:
        self.add_comment("Crear directorio del proyecto")
        self.add_print("Crear directorio del proyecto")
        self._script.add(f'PROJECT_NAME="{project_anme}"')
        self._script.add("mkdir $PROJECT_NAME")
        self._script.add("cd $PROJECT_NAME")
    
    def add_command(self, command: str) -> None:
        self._script.add(command)
    
    def add_create_file(self, path_file: str) -> None:
        self._script.add("touch "+path_file)
    
    def add_write_to_file(self, path_file: str, content_file: ConcreteScript) -> None:
        self._script.add("cat <<EOT > "+path_file)
        for line in content_file._parts:
            self._script.add(line)
        self._script.add("EOT")
