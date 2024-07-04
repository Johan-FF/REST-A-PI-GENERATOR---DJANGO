from __future__ import annotations
from .builder import Builder
import os

class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing scripts according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self) -> None:
        self._builder = None

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
        self.create_script_file(self._builder.script)

    def build_django_api_rest(self) -> None:
        pass

    """
    Creation of .sh file.
    """
    def create_script_file(self, content: str):
        # Obtener la ruta del directorio actual (donde está el script)
        current_dir = os.path.dirname(__file__)

        # Construir la ruta a la carpeta2
        target_dir = os.path.join(current_dir, '..', 'fastapi')

        # Asegurarse de que la carpeta2 existe
        os.makedirs(target_dir, exist_ok=True)

        # Ruta completa del archivo que se creará en carpeta2
        file_path = os.path.join(target_dir, 'prueba.sh')

        # Crear y escribir en el archivo
        with open(file_path, 'w') as file:
            file.write(content.parts_as_string())
 
        file.close()

# if __name__ == "__main__":
#     """
#     The client code creates a builder object, passes it to the director and then
#     initiates the construction process. The end result is retrieved from the
#     builder object.
#     """

#     director = Director()
#     builder = ConcreteBuilder1()
#     director.builder = builder

#     print("Standard basic product: ")
#     director.build_minimal_viable_product()
#     builder.product.list_parts()

#     print("\n")

#     print("Standard full featured product: ")
#     director.build_full_featured_product()
#     builder.product.list_parts()

#     print("\n")

#     # Remember, the Builder pattern can be used without a Director class.
#     print("Custom product: ")
#     builder.produce_part_a()
#     builder.produce_part_b()
#     builder.product.list_parts()