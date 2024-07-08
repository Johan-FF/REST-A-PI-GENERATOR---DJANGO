from .create_script import CreateScript
from ..concrete_script import ConcreteScript

class WindowsCreator(CreateScript):
    """
    Concrete classes have to implement all abstract operations of the base
    class. They can also override some operations with a default implementation.
    """

    def __init__(self) -> None:
        super().__init__()
        self._script.add("@echo off")

    def add_comment(self, comment: str) -> None:
        self._script.add("rem "+comment)
    
    def add_print(self, msg: str) -> None:
        self._script.add("echo "+msg)
    
    def add_enter_project_packague(self, project_anme: str) -> None:
        self.add_comment("Crear directorio del proyecto")
        self.add_print("Crear directorio del proyecto")
        self._script.add(f'set "PROJECT_NAME={project_anme}"')
        self._script.add("mkdir %PROJECT_NAME%")
        self._script.add("cd %PROJECT_NAME%")
    
    def add_command(self, command: str) -> None:
        self._script.add(command)
    
    def add_call(self, path_bat_file: str) -> None:
        self._script.add("call "+path_bat_file+".bat")
    
    def add_create_file(self, path_file: str) -> None:
        self._script.add("type NUL > "+path_file)
    
    def add_write_to_file(self, path_file: str, content_file: ConcreteScript) -> None:
        self._script.add("(")
        for line in content_file._parts:
            if line=="\n":
                self._script.add("echo.")
                continue
            self._script.add("echo "+self._add_caret_before_quotes(line))
        self._script.add(") > "+path_file)

    def _add_caret_before_keywords(self, content: str) -> str:
        result: str = ''
        for char in content:
            if char == '"':
                result += '^"'
            elif char == "'":
                result += "^'"
            elif char == "(":
                result += "^("
            elif char == ")":
                result += "^)"
            else:
                result += char
        return result
