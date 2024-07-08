import os

from .utils.data_types import get_python_type
from .builder import Builder
from .concrete_script import ConcreteScript

class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing scripts according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self) -> None:
        self._builder: Builder = None
        self._so: str = ""

    @property
    def so(self) -> str:
        return self._so

    @so.setter
    def so(self, so: str) -> None:
        self._so = so

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled script.
        """
        self._builder = builder

    """
    The Director can construct several script variations using the same
    building steps.
    """

    def build_nest_js_api_rest(self) -> None:
        pass

    def build_fast_api_api_rest(self, csm_model, relational_model) -> None:
        entities: list[str] = []

        for table in relational_model.findall("table"):
            
            attributes: list[dict] = []
            for attribute in table.find("attributes").findall("attribute"):
                attributes.append({
                    "name": attribute.get("name"),
                    "is-pk":  True if attribute.get("PK")=="true" else False,
                    "data-type":  get_python_type(attribute.get("data-type")),
                })

            relations: dict[str, str] = {}
            for relation in table.find("relations").findall("relation"):
                relations[relation.get("attribute")] = relation.get("table")

            table_name: str = table.get("name")
            entities.append(table_name)
            self._builder.produce_crud(table_name, attributes, relations)
        
        self._builder.produce_app_file(entities)

        self.create_script_file(self._builder.script)


    def build_django_api_rest(self) -> None:
        pass

    """
    Creation of .sh file.
    """
    def create_script_file(self, content: ConcreteScript):
        current_dir = os.path.dirname(__file__)

        target_dir = os.path.join(current_dir, '..', 'fastapi')

        os.makedirs(target_dir, exist_ok=True)

        file_name = 'prueba.'+ ("bat" if self._so=="WINDOWS" else "sh")
        file_path = os.path.join(target_dir, file_name)

        with open(file_path, 'w') as file:
            file.write(content.parts_as_string())
 
        file.close()
