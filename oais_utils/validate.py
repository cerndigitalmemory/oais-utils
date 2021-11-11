import logging
import json
import os
import bagit
from jsonschema import validate
from .schemas import draft


# Verify if folder exists
def verify_folder_exists(path):
    logging.info(f"Verifying if folder {path} exists.")
    if not os.path.exists(path):
        raise Exception(f"Directory {path} does not exist.")


# Verify bag
def verify_bag(path, is_dry=False):
    bag = bagit.Bag(path)
    try:
        bag.validate()
    except bagit.BagValidationError as e:
        for d in e.details:
            if isinstance(d, bagit.FileMissing):
                if not is_dry:
                    raise Exception(
                        "%s exists in manifest but was not found on filesystem"
                    ) % (d.path)
    except:
        raise Exception(f"Bag validation error")


def verify_directory_structure(path, dirlist):
    logging.info("Verifying directory structure")
    for directory in dirlist:
        dir_path = os.path.join(path, directory)
        logging.info(f"Checking if {dir_path} exists")
        if not os.path.exists(dir_path):
            raise Exception(f"Directory {dir_path} does not exist.")
        else:
            logging.info(f"\tSuccessful")


# Check whether sip.json contains the required fields
def validate_sip(path, schema, sip_json_name="sip.json"):
    logging.info("Validating sip.json")
    try:
        for root, dirs, files in os.walk(path):
            if sip_json_name in files:
                sip_file = os.path.join(root, sip_json_name)
                with open(sip_file) as json_file:
                    data = json.load(json_file)

                # Get the json as a from draft function.
                check_schema = draft(schema)

                validate(instance=data, schema=check_schema)

                logging.info(f"\tValidated successfully against the {schema}")
                return sip_file

    except:
        logging.info("Sip validation failed.")


# Check if the content folder exists and contains all the files
def validate_contents(path, sip_file):
    logging.info("Validate contents folder")

    with open(sip_file) as json_file:
        data = json.load(json_file)

    is_dry = data["audit"][0]["tool"]["params"]["dry_run"]

    if not is_dry:
        try:
            content_files = data["contentFiles"]
            for file in content_files:
                bagpath = file["bagpath"]
                downloaded = file["downloaded"]
                if downloaded:
                    full_bagpath = os.path.join(path, bagpath)
                    if os.path.exists(full_bagpath):
                        logging.info(f"\tFile in path: {bagpath} exists")
                    else:
                        raise Exception(f"File in path: {bagpath} does not exist")
            return False
        except:
            raise Exception("Error with the contentFiles")
    else:
        logging.info(f"This is a dry_run bag. Searching for fetch.txt...")
        # Check if fetch.txt is actually there
        if os.path.isfile(os.path.join(path, "fetch.txt")):
            logging.info(f"\tSuccessful")
        else:
            raise Exception(f"\tfetch.txt was not found inside {path}")
        return True


# Validate data according to SIP specification
def validate_sip_folder(path, schema="draft1"):
    logging.basicConfig(level=20, format="%(message)s")
    logging.info("Starting validation")

    try:
        verify_folder_exists(path)

        verify_directory_structure(path, dirlist=["data", "data/content", "data/meta"])

        sip_file = validate_sip(path, schema)

        is_dry = validate_contents(path, sip_file)

        verify_bag(path, is_dry)

        logging.info("Validation ended successfully.")

        return {"status": 0, "errormsg": None}
    except Exception as e:
        logging.error(f"Validation failed with error: {e}")

        return {"status": 1, "errormsg": e}
