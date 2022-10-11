import json
import statistics
import zipfile
from typing import Dict, List

import dateutil.parser
import pandas
from sail_safe_functions_orchestrator.data_frame_logitudinal import DataFrameLogitudinal


class ReadZipJsonFhirPrecompute:
    def run(path_file_jsonzip_source: str):
        # 1. Covert patients into events
        list_patient = []
        with zipfile.ZipFile(path_file_jsonzip_source, "r") as zip_file:
            for name_file in zip_file.namelist():  # TODO change to all
                if ".json" not in name_file:
                    continue

                patient = json.loads(zip_file.read(name_file))
                list_patient.append(ReadZipJsonFhirPrecompute.process_patient(patient))
        return DataFrameLogitudinal(list_patient)

    def process_patient(dict_patient):
        # step 1 find the patient resource
        patient = {}
        patient["resource"] = ""
        patient["dict_measurement"] = {}
        for entry in dict_patient["entry"]:
            # TODO packaging, check that there is only one patient resource per file and that all events relate to that patient
            if "Patient" == entry["resource"]["resourceType"]:
                patient["resource"] = entry["resource"]

        list_event = []
        for entry in dict_patient["entry"]:
            resource = entry["resource"]
            list_event.extend(ReadZipJsonFhirPrecompute.parse_list_event(resource))

        # print(f"{name_file} {len(dict)} {dict.keys()}")
        for event in list_event:
            measurement = event["event_type"]  # TODO rename?
            if measurement not in patient["dict_measurement"]:
                patient["dict_measurement"][measurement] = []
            patient["dict_measurement"][measurement].append(event)

        # sort measurements by date
        for measurement in patient["dict_measurement"]:
            patient["dict_measurement"][measurement] = sorted(
                patient["dict_measurement"][measurement], key=lambda measurement_val: measurement_val["datetime_object"]
            )

        return patient

    def parse_list_event(resource):
        list_event = []
        resource_type = resource["resourceType"]
        try:
            if resource_type == "Encounter":
                event_type = resource_type + ":" + resource["type"][0]["coding"][0]["display"]
                event_value = resource["status"]
                datetime_object = dateutil.parser.isoparse(resource["period"]["start"])

            elif resource_type == "Condition":
                event_type = resource_type + ":" + resource["code"]["coding"][0]["display"]
                event_value = resource["verificationStatus"]["coding"][0]["code"]
                datetime_object = dateutil.parser.isoparse(resource["recordedDate"])
                list_event.append(
                    {"event_type": event_type, "event_value": event_value, "datetime_object": datetime_object}
                )

            elif resource_type == "Observation":
                datetime_object = dateutil.parser.isoparse(resource["effectiveDateTime"])
                if "component" in resource:
                    for component in resource["component"]:
                        event_type = resource_type + ":" + component["code"]["coding"][0]["display"]
                        event_value = component["valueQuantity"]["value"]
                        list_event.append(
                            {"event_type": event_type, "event_value": event_value, "datetime_object": datetime_object}
                        )
                else:
                    event_type = resource_type + ":" + resource["code"]["coding"][0]["display"]
                    if "valueQuantity" in resource:
                        event_value = resource["valueQuantity"]["value"]
                    elif "valueString" in resource:
                        event_value = resource["valueString"]
                    else:
                        event_value = resource["valueCodeableConcept"]["coding"][0]["display"]

                    # TODO add unit?
                    list_event.append(
                        {"event_type": event_type, "event_value": event_value, "datetime_object": datetime_object}
                    )

            elif resource_type == "Procedure":
                event_type = resource_type + ":" + resource["code"]["coding"][0]["display"]
                event_value = resource["status"]
                datetime_object = dateutil.parser.isoparse(resource["performedPeriod"]["start"])

                list_event.append(
                    {"event_type": event_type, "event_value": event_value, "datetime_object": datetime_object}
                )

            elif resource_type == "MedicationRequest":
                event_type = resource_type + ":" + resource["medicationCodeableConcept"]["coding"][0]["display"]
                event_value = resource["status"]
                datetime_object = dateutil.parser.isoparse(resource["authoredOn"])
                list_event.append(
                    {"event_type": event_type, "event_value": event_value, "datetime_object": datetime_object}
                )

            elif resource_type == "Immunization":
                event_type = resource_type + ":" + resource["vaccineCode"]["coding"][0]["display"]
                event_value = resource["status"]
                datetime_object = dateutil.parser.isoparse(resource["occurrenceDateTime"])
                list_event.append(
                    {"event_type": event_type, "event_value": event_value, "datetime_object": datetime_object}
                )

        except Exception as exception:
            print(json.dumps(resource, indent=4, sort_keys=True))
            print(resource_type)
            raise exception
        # if 0 < len(list_event):
        #     print(event_type)
        #     print(event_value)
        #     print(datetime_object)

        return list_event


#    def event_selector first, last
# measurement selector value_of, seconds_between
