import logging
import json
import os

# Extract given field from json dictonary
def get_field_from_json(data, field):
    try:
        if not data[field]:
            raise Exception(f"Required 'bic-meta.json' field: {field} is empty.")
        else:
            logging.info(f"\tFound field: {field}")
        return data[field]
    except KeyError:
        raise Exception(f"'bic-meta.json' does not contain a required field: {field}")


# Verify if folder exists
def verify_folder_exists(path):
    logging.info(f"Verifying if folder {path} exists.")
    if not os.path.exists(path):
        raise Exception(f"Directory {path} does not exist.")


# Verify whether AIU and AIC directories exists
def verify_directory_structure(path):
    logging.info("Verifying directory structure")

    data_path = os.path.join(path, "data")
    if not os.path.exists(data_path):
        raise Exception("Directory named 'data' does not exist.")

    aic_folder = None
    bagit_txt = False
    baginfo_txt = False

    for dir in os.listdir(path):

        if dir == "bagit.txt":
            logging.info("Verifying bagit.txt file..")
            bagit_txt = True

        if dir == "bag-info.txt":
            logging.info("Verifying bag-info.txt file..")
            baginfo_txt = True

    for dir in os.listdir(data_path):
        logging.info("Verifying data/content folder..")
        if os.path.isdir(os.path.join(data_path, "content")):
            logging.info("Content folder exists..")
        logging.info("Verifying data/meta folder..")
        dir_path = os.path.join(data_path, "meta")
        if os.path.isdir(dir_path):
            logging.info("Meta folder exists..")

            for sub in os.listdir(dir_path):
                empty = False
                if "sip.json" in sub:
                    is_aic = True

            if empty:
                raise Exception(f"Empty directory found: {dir_path}")

            if is_aic:
                aic_folder = dir_path
                logging.info(f"\tFound AIC file directory: {dir_path}")
            else:
                logging.info(f"\tFound AIU file directory: {dir_path}")

    if not bagit_txt:
        raise Exception("bagit.txt was not found.")
    if not baginfo_txt:
        raise Exception("bag-info.txt was not found.")
    if not aic_folder:
        raise Exception("AIC directory was not found.")

    return aic_folder


# Check whether bic-meta.json contains the required fields
def validate_bic_meta(path, aic_folder):
    logging.info("Validating sip.json")
    try:
        with open(os.path.join(aic_folder, "sip.json")) as json_file:
            data = json.load(json_file)

            required_fields = ["metadataFile_upstream", "contentFiles"]
            for field in required_fields:
                get_field_from_json(data, field)

    except FileNotFoundError:
        raise Exception("bic-meta.json file not found.")


# Validate data according to the CERN AIP specification
def validate_aip(path):
    logging.basicConfig(level=20, format="%(message)s")
    logging.info("Starting validation")

    try:
        verify_folder_exists(path)

        aic_folder = verify_directory_structure(path)

        validate_bic_meta(path, aic_folder)

        logging.info("Validation ended successfully.")

        return {"status": 0, "errormsg": None}
    except Exception as e:
        logging.error(f"Validation failed with error: {e}")

        return {"status": 1, "errormsg": e}
