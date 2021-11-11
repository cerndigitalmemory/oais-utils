import json
import logging
import os

# This function gets the json drafts (now from the schemas folder later from a git source) and returns a dictionary with the values and paths
def get_draft_dict():
    json_drafts = {"draft1": "oais_utils/schemas/sip-schema-d1.json"}
    return json_drafts


# function to get the JSON list from the dictionary
def draftlist():
    drafts = get_draft_dict()
    return_list = []
    for draft in drafts.keys():
        return_list.append(draft)
    return return_list


# A function to get a specific version
def draft(draft_version):
    logging.info(f"Getting {draft_version}.")
    drafts = get_draft_dict()
    try:
        path = drafts[draft_version]
        with open(path) as f:
            draftedJSON = json.load(f)
            logging.info(f"/t{draft_version} found successfully")

    except:
        raise Exception(f"Version {draft_version} was not found!")
    return draftedJSON
