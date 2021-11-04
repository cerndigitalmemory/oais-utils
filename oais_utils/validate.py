import logging
import json
import os
import bagit
from jsonschema import validate


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
    if not os.path.exists(data_path):
        raise Exception("Directory named 'data' does not exist.")

    sip_folder = None

    for dir in os.listdir(data_path):
        logging.info("Verifying data/content folder..")
        if os.path.isdir(os.path.join(data_path, "content")):
            logging.info("Content folder exists..")
        logging.info("Verifying data/meta folder..")
        dir_path = os.path.join(data_path, "meta")
        if os.path.isdir(dir_path):
            logging.info("Meta folder exists..")

            for sub in os.listdir(dir_path):
                if "sip.json" in sub:
                    is_sip = True

            if is_sip:
                sip_folder = dir_path
                logging.info(f"\tFound SIP file directory: {sip_folder}")
            else:
                raise Exception(f"Empty directory found: {dir_path}")

    if not sip_folder:
        raise Exception("sip directory was not found.")

    return sip_folder


# Check whether sip.json contains the required fields
def validate_sip(sip_folder):
    logging.info("Validating sip.json")
    try:

        with open(os.path.join(sip_folder, "sip.json")) as json_file:
            data = json.load(json_file)

        with open("sip-schema-d1.json") as json_schema:
            schema = json.load(json_schema)

        validate(instance=data, schema=schema)

    except Exception as err:
        print(err)


# Validate data according to SIP specification
def validate_sip_folder(path):
    logging.basicConfig(level=20, format="%(message)s")
    logging.info("Starting validation")

    try:
        verify_folder_exists(path)

        verify_bag(path)

        sip_folder = verify_directory_structure(path)

        validate_sip(path, sip_folder)

        logging.info("Validation ended successfully.")

        return {"status": 0, "errormsg": None}
    except Exception as e:
        logging.error(f"Validation failed with error: {e}")

        return {"status": 1, "errormsg": e}
