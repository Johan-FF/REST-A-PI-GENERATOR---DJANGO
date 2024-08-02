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

    def build_nest_js_api_rest(self, relational_model) -> None:
        entities: list[str] = []
        for table in relational_model.findall("table"):
            
            attributes: list[dict] = []
            for attribute in table.find("attributes").findall("attribute"):
                attributes.append({
                    "name": attribute.get("name"),
                    "is-pk":  True if attribute.get("PK")=="true" else False,
                    "is-fk": True if attribute.get("FK")=="true" else False,
                    "nn": "true" if attribute.get("NN")=="true" else "false",
                    "uq": "true" if attribute.get("UQ")=="true" else "false",
                    "ai": "true" if attribute.get("AI")=="true" else "false",
                    "data-type":  attribute.get("data-type"),
                })
            
            relations: list[dict] = []
            try:
                for relation in table.find("relations").findall("relation"):
                    relations.append({"table": relation.get("table"),
                                      "attribute": relation.get("attribute")})
            except AttributeError:
                pass
            
            multiplicity_relations: list[dict] = []
            for aux_table in relational_model.findall("table"):  
                if table.get("name") != aux_table.get("name"):
                    try:
                        for aux_relation in aux_table.find("relations").findall("relation"):
                            if aux_relation.get("table") == table.get("name"):
                                multiplicity_relations.append({
                                    "table": aux_table.get("name"),
                                    "multiplicity": aux_relation.get("multiplicity")
                                })
                    except AttributeError:
                        pass
            
            table_name: str = table.get("name")
            entities.append(table_name)
            self._builder.produce_crud(table_name, attributes, relations, multiplicity_relations)

        self._builder.produce_app_file(entities)
            
        self.create_script_file(self._builder.script)
        

    def build_fast_api_api_rest(self, relational_model) -> None:
        entities: list[str] = []

        multiplicity_relations: dict[str, str] = {}
        for table in relational_model.findall("table"):
            try:
                for relation in table.find("relations").findall("relation"):
                    multiplicity_relations[relation.get("table")] = table.get("name")
            except AttributeError:
                break

        for table in relational_model.findall("table"):
            
            attributes: list[dict] = []
            for attribute in table.find("attributes").findall("attribute"):
                attributes.append({
                    "name": attribute.get("name"),
                    "is-pk":  True if attribute.get("PK")=="true" else False,
                    "is-fk":  True if attribute.get("FK")=="true" else False,
                    "is-nn":  True if attribute.get("NN")=="true" else False,
                    "is-uq":  True if attribute.get("UQ")=="true" else False,
                    "is-ai":  True if attribute.get("AI")=="true" else False,
                    "data-type":  get_python_type(attribute.get("data-type")),
                })

            relations: dict[str, str] = {}
            try:
                for relation in table.find("relations").findall("relation"):
                    relations[relation.get("attribute")] = relation.get("table")
            except AttributeError:
                pass

            table_name: str = table.get("name")
            entities.append(table_name)
            self._builder.produce_crud(table_name, attributes, relations, multiplicity_relations)
        
        self._builder.produce_app_file(entities)

        self.create_script_file(self._builder.script)

    """
    Creation of .sh file.
    """
    def create_script_file(self, content: ConcreteScript):
        
        current_dir = os.path.dirname(__file__)

        target_dir = os.path.join(current_dir, '..', 'fastapi')

        os.makedirs(target_dir, exist_ok=True)
        
        file_name = 'prueba2.'+ ("bat" if self._so=="WINDOWS" else "sh")
        file_path = os.path.join(target_dir, file_name)

        with open(file_path, 'w') as file:
            file.write(content.parts_as_string())
 
        file.close()
