# app/xml_validator.py

import xmlschema

XSD_SCHEMA_PATH = "./schemas/openimmo_127c.xsd"

def validate_xml(xml_file: str) -> bool:
    schema = xmlschema.XMLSchema(XSD_SCHEMA_PATH)
    try:
        schema.validate(xml_file)
        return True
    except xmlschema.XMLSchemaValidationError:
        return False
