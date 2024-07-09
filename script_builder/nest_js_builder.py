from .script_method.windows_script import WindowsCreator
from .script_method.linux_script import LinuxCreator
from .builder import Builder
from script_builder.concrete_script import ConcreteScript
from .utils.data_types import types_to_valid_sqlalchemy_types, \
                            remove_special_characters_and_capitalize, \
                            type_to_valid_sqlalchemy_type

class NestApiBuilder(Builder):
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
        NestApiBuilder.OPERATING_SYSTEM = psm_model.find("so").get("so-name")

        project_name = psm_model.find("project").get("name")
        NestApiBuilder.PROJECT_NAME = project_name

        technology = psm_model.find("technology")
        NestApiBuilder.EXECUTE_PORT = technology.get("port")
        NestApiBuilder.VERSION = technology.get("version")

        self.reset()
        
    def reset(self) -> None:
        self._script = ConcreteScript()
        print()
        if NestApiBuilder.OPERATING_SYSTEM=="WINDOWS":
            self.script_method = WindowsCreator()
        else:
            self.script_method = LinuxCreator()
        self.script_method.add_comment("Nombre del proyecto")
        self.script_method.add_enter_project_packague(NestApiBuilder.PROJECT_NAME)
        
        self.script_method.add_command(f"nest new {NestApiBuilder.PROJECT_NAME}")
        
        
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
        script = self.script_method._script
        self.reset()
        return script
    
    def produce_create(self):
        pass

    def produce_crud(self):
        pass    
    
    def produce_delete(self):
        pass 
    
    def produce_read(self):
        pass
    def produce_update(self):
        pass
    
    
        
        
        
        
