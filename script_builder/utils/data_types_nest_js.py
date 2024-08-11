
type_mapping = {
    'BOOL': 'boolean',
    'INT': 'number',
    'FLOAT': 'number',
    'DECIMAL': 'number',
    'VARCHAR': 'string',
    'BINARY': 'boolean',
    'DATE': 'Date',
    'DATETIME': 'Date',
}

def get_javascript_type(data_type_str: str) -> str:
    return type_mapping.get(data_type_str, '')

type_orm_data_types = {
    'BOOL': 'boolean',
    'INT': 'integer',
    'FLOAT': 'float',
    'DECIMAL': 'float',
    'VARCHAR': 'varchar',
    'BINARY': 'binary',
    'DATE': 'date',
    'DATETIME': 'datetime',
}

def types_to_valid_type_orm_types(attributes: list) -> str:
    final_types = set()
    
    for attribute in attributes:
        data_type = attribute.get("data-type")
        final_types.add(type_orm_data_types[data_type])
    
    return ", ".join(final_types)

def type_to_valid_type_orm_type(type: type) -> str:
    return type_orm_data_types.get(type, "")

type_validator = {
    'INT': "IsNumber",
    'VARCHAR': "IsString",
    'FLOAT': "IsNumber",
    'DECIMAL': "IsNumber", 
    'BOOL': "IsBoolean",
    'BINARY': "IsBoolean",
    'DATE': "IsDate",
    'DATETIME': " IsDate"
}

def get_validator_type(type: type) -> str:
    return type_validator.get(type, "")
