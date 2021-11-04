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
    content_flag = False
    meta_flag = False

    for directory in os.listdir(data_path):
        print(directory, data_path)
        logging.info("Verifying data folder contents..")
        content_folder = os.path.join(data_path, "content")
        print(content_folder)
        if directory == "content":
            logging.info("Content folder exists..")
            content_flag = True

        meta_folder = os.path.join(data_path, "meta")
        if directory == "meta":
            is_sip = False
            logging.info("Meta folder exists..")
            for sub in os.listdir(meta_folder):
                if "sip.json" in sub:
                    is_sip = True

            if is_sip:
                sip_folder = directory
                logging.info(f"\tFound SIP file directory: {sip_folder}")
            else:
                raise Exception(f"Empty directory found: {dir_path}")
        else:
            raise Exception(f"Meta folder does not exist in {directory}")

    if not sip_folder:
        raise Exception("Sip directory was not found.")

    if not content_flag:
        raise Exception(f"Content folder does not exist in {data_path}")
    if not meta_flag:
        raise Exception(f"Mefolder does not exist in {data_path}")

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

        validate_sip(sip_folder)

        logging.info("Validation ended successfully.")

        return {"status": 0, "errormsg": None}
    except Exception as e:
        logging.error(f"Validation failed with error: {e}")

        return {"status": 1, "errormsg": e}
