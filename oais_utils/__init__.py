import oais_utils.validate
import os.path
import json

# Make the json schemas paths relative to the __init__.py file location so when called externally the schemas folder will be found (e.g. OAIS Platform)
relative_path = os.path.join(os.path.dirname(__file__), "schemas/sip-schema-d1.json")
json_schemas_paths = {"draft1": relative_path}


def schemas():
    """
    Retrieves every JSON schema file defined in the "schemas_path",
    reading them from disk and returning an Object
    { 'schema_name' -> schema_dict }
    """
    json_schemas = {}
    # For every schema mentioned
    for schema_name in json_schemas_paths:
        # Read the file it points it
        with open(json_schemas_paths[schema_name]) as f:
            # as a JSON file
            json_schemas[schema_name] = json.load(f)

    return json_schemas
