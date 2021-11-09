import logging
import json
import os
import bagit
from jsonschema import validate
from schemas import draft


# Verify if folder exists
def verify_folder_exists(path):
    logging.info(f"Verifying if folder {path} exists.")
    if not os.path.exists(path):
        raise Exception(f"Directory {path} does not exist.")


# Verify bag
def verify_bag(path):
    bag = bagit.Bag(path)
    valid = False
    try:
        valid = bag.validate()
    except bagit.BagValidationError as err:
        print(f"Bag validation failed: {err}")
    if not valid:
        raise Exception(f"Bag validation error")


# Verify whether SIP directory exists
def verify_directory_structure(path):
    logging.info("Verifying directory structure")

    data_path = os.path.join(path, "data")
    content_path = os.path.join(data_path, "content")
    meta_path = os.path.join(data_path, "meta")

    paths = [data_path, content_path, meta_path]

    for path in paths:
        logging.info(f"Checking if {path} exists")
        if not os.path.exists(path):
            raise Exception(f"Directory {path} does not exist.")
        else:
            logging.info(f"\tSuccessful")

    return meta_path


# Check whether sip.json contains the required fields
def validate_sip(sip_folder, schema):
    logging.info("Validating sip.json")
    try:

        with open(os.path.join(sip_folder, "sip.json")) as json_file:
            data = json.load(json_file)

        # Get draft0 from draft function.
        schema = draft()

        validate(instance=data, schema=schema)

    except Exception as err:
        print(err)


# Validate data according to SIP specification
def validate_sip_folder(path, schema="draft1"):
    logging.basicConfig(level=20, format="%(message)s")
    logging.info("Starting validation")

    try:
        verify_folder_exists(path)

        verify_bag(path)

        sip_folder = verify_directory_structure(path)

        validate_sip(sip_folder, schema)

        logging.info("Validation ended successfully.")

        return {"status": 0, "errormsg": None}
    except Exception as e:
        logging.error(f"Validation failed with error: {e}")

        return {"status": 1, "errormsg": e}
