# import oais_utils.validate

json_schemas_paths = {"draft1": "oais_utils/schemas/sip-schema-d1.json"}

import json


def schemas():
    json_schemas = {}
    for schema_name in json_schemas_paths:
        with open(json_schemas_paths[schema_name]) as f:
            json_schemas[schema_name] = json.load(f)

    return json_schemas
