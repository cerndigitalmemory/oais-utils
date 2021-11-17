import json

# List available JSON schemas
# schema_name -> schema_path
json_schemas_paths = {"draft1": "oais_utils/schemas/sip-schema-d1.json"}


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
