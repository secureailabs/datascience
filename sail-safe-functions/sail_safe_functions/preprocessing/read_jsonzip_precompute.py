import json
import statistics
import zipfile
from typing import Dict, List

import dateutil.parser
import pandas


class ReadJsonzipPrecompute:
    def run(path_file_jsonzip_source: str, dict_feature_schema):
        dict_feature_template = dict_feature_schema["dict_column"]
        # 1. Covert patients into events
        list_patient = []
        with zipfile.ZipFile(path_file_jsonzip_source, "r") as zip_file:
            for name_file in zip_file.namelist():  # TODO change to all
                if ".json" not in name_file:
                    continue

                dict_patient = json.loads(zip_file.read(name_file))
                list_patient.append(ReadJsonzipPrecompute.process_patient(dict_patient))

        # 2. Compute statistics on events
        dict_measurement_statistics = ReadJsonzipPrecompute.compute_statistics(list_patient)

        # 3. List all categories by fraction of patients that have at least 1
        do_list_data = False
        if do_list_data:
            for key, value in sorted(
                dict_measurement_statistics.items(),
                key=lambda key_value: key_value[1]["count_atleastone"],
                reverse=True,
            ):
                count = value["count_atleastone"] / len(list_patient)
                print(f"{key} {count}")

        # 4. convert mesurements to table
        dict_column = {}
        for name_feature in dict_feature_template:
            dict_column[name_feature] = []

        for patient in list_patient:
            ReadJsonzipPrecompute.compile_columns(dict_column, dict_feature_template, patient)

        data_frame = pandas.DataFrame()
        for name_feature in dict_feature_template:
            data_frame[name_feature] = pandas.Series(data=dict_column[name_feature], name=name_feature)

        return data_frame

    def compile_columns(dict_series: Dict[str, List], dict_feature_template: Dict, patient):
        for name_column, column_template in dict_feature_template.items():
            feature_value = ReadJsonzipPrecompute.compile_column(column_template, patient)
            dict_series[name_column].append(feature_value)

    def compile_column(column_template, patient):
        type_feature = column_template["type_feature"]
        try:
            # patient resource lookup
            # TODO refactor this
            if type_feature == "patient_gender":
                return patient["resource"]["gender"]
                # TODO there is also this attribute
                #          {
                #     "url": "http://hl7.org/fhir/us/core/StructureDefinition/us-core-birthsex",
                #     "valueCode": "F"
                # },
            elif type_feature == "patient_marital_status":
                return patient["resource"]["maritalStatus"]["coding"][0]["display"]
            elif type_feature == "patient_race":
                for extension in patient["resource"]["extension"]:
                    if extension["url"] == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-race":
                        return extension["extension"][0]["valueCoding"]["display"]
                return None
            elif type_feature == "patient_ethnicity":
                for extension in patient["resource"]["extension"]:
                    if extension["url"] == "http://hl7.org/fhir/us/core/StructureDefinition/us-core-ethnicity":
                        return extension["extension"][0]["valueCoding"]["display"]
                return None

            elif type_feature == "numeric":
                # TODO also enforce resolution, and add that to the schema
                name_measurement = column_template["name_measurement"]
                type_selector = column_template["type_selector"]
                if name_measurement not in patient["dict_measurement"]:
                    if type_selector == "count_occurance":
                        return 0
                    else:
                        return None

                list_measurement = patient["dict_measurement"][name_measurement]
                if type_selector == "first_occurance":
                    return list_measurement[0]["event_value"]
                if type_selector == "last_occurance":
                    return list_measurement[-1]["event_value"]
                if type_selector == "count_occurance":
                    return len(list_measurement)
                if type_selector == "mean":
                    list_measurement_value = [measurement["event_value"] for measurement in list_measurement]
                    return statistics.mean(list_measurement_value)

                else:
                    raise Exception(f"unkown type_selector {type_selector}")

            elif type_feature == "categorical":
                name_measurement = column_template["name_measurement"]
                type_selector = column_template["type_selector"]
                if name_measurement not in patient["dict_measurement"]:
                    if type_selector == "count_occurance":
                        return 0
                    else:
                        return None

                list_measurement = patient["dict_measurement"][name_measurement]
                if type_selector == "first_occurance":
                    return list_measurement[0]["event_value"]
                if type_selector == "last_occurance":
                    return list_measurement[-1]["event_value"]
                if type_selector == "count_occurance":
                    return len(list_measurement)
                if type_selector == "most_frequent":
                    raise NotImplementedError()  # TODO implement
                else:
                    raise Exception(f"unkown type_selector {type_selector}")

            else:
                raise Exception(f"unkown type_feature {type_feature}")

        except Exception as exception:
            print(json.dumps(patient["resource"], indent=4, sort_keys=True))
            raise exception
        raise Exception(f"cannot return default")

    def compute_statistics(list_patient):
        dict_measurement_statistics = {}
        for patient in list_patient:
            for measurement in patient["dict_measurement"]:
                if measurement not in dict_measurement_statistics:
                    dict_measurement_statistics[measurement] = {}
                    dict_measurement_statistics[measurement]["count_atleastone"] = 0
                    dict_measurement_statistics[measurement]["count_total"] = 0
                    dict_measurement_statistics[measurement]["list_count"] = []
                    dict_measurement_statistics[measurement]["gini"] = 0  # TODO

                dict_measurement_statistics[measurement]["count_atleastone"] += 1
                dict_measurement_statistics[measurement]["count_total"] += len(patient["dict_measurement"][measurement])
                dict_measurement_statistics[measurement]["list_count"].append(
                    len(patient["dict_measurement"][measurement])
                )
        return dict_measurement_statistics

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
            list_event.extend(ReadJsonzipPrecompute.parse_list_event(resource))

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
