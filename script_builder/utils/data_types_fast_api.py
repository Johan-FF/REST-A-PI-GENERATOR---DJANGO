import re

type_mapping = {
    'BOOL': bool,
    'INT': int,
    'DECIMAL': float,
    'VARCHAR': str,
    'BINARY': bytes
}

def get_python_type(data_type_str: str) -> type:
    return type_mapping.get(data_type_str, None)

sqlalchemy_data_types = {
    bool: "Boolean",
    int: "Integer",
    float: "Float",
    str: "String",
    bytes: "LargeBinary"
}

def types_to_valid_sqlalchemy_types(attributes: list):
    final_types = set()
    
    for attribute in attributes:
        data_type = attribute.get("data-type")
        final_types.add(sqlalchemy_data_types[data_type])
    
    return ", ".join(final_types)

def type_to_valid_sqlalchemy_type(type: type):
    return sqlalchemy_data_types[type]

def remove_special_characters_and_capitalize(string: str):
    words = re.findall(r'[a-zA-Z]+', string)
    return ''.join(word.capitalize() for word in words)
