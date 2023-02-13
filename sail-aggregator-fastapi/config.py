import os
import json
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference
from sail_safe_functions.aggregator.statistics import count

dataframe_name_lookup = {}

# TODO: attempt to make things prettier but these were not findable inside routers
# global scn_names
# global scn_ports
# global list_dataset_id
# global IV_SETTINGS_FILE
# global service_reference

scn_names = []
scn_ports = []
list_dataset_id = []
IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")
service_reference = TestServiceReference.get_instance()

MINIMUM_SAMPLE_SIZE = 0

def query_limit_n(series, n = MINIMUM_SAMPLE_SIZE) -> bool:
    """
    Checks data or series in question is over a given threshold.

    :param: data: the data item being checked
    :type: remote dataframe or remote series
    :return: True or False relating to whether the threshold has been surpassed
    :type: Boolean
    """
    return count(series) > n

async def validate(series):
    """
    Validates execution criteria for data inputs
    :param: data: the data item being validated
    :type: Remote Dataframe or Remote Series
    :return: None
    :type: None
    """
    if not query_limit_n(series):
        message = "Validation Failure: Sample size too small"
        await log_validation_failure(message)
        raise HTTPException(status_code=500, detail=message)
    else:
        return



if os.environ.get("IV_FILEPATH") is not None:
    IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

with open(IV_SETTINGS_FILE) as initial_settings:
    configuration = json.load(initial_settings)
    for entry in configuration["secure_computation_nodes"]:
        scn_names.append(entry["ip_address"])
        scn_ports.append(5556)
        list_dataset_id.append(entry["dataset_id"])
