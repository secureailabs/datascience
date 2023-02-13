from sail_safe_functions.test.helper_sail_safe_functions.participant_service_local import ParticipantSeriviceLocal
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference
from sail_core.implementation.participant_service_client_dict import ParticipantServiceClientDict
from sail_core.implementation_manager import ImplementationManager
from routers import data_model, data_ingestion, data_manipulation, preprocessing, statistics, visualization


from fastapi import FastAPI
import aggregator_node

app = FastAPI()

# app.include_router(aggregator_node.router)
app.include_router(data_model.router)
app.include_router(data_ingestion.router)
app.include_router(data_manipulation.router)
app.include_router(preprocessing.router)
app.include_router(statistics.router)
app.include_router(visualization.router)





implementation_manager = ImplementationManager.get_instance()
implementation_manager.set_participant_service(ParticipantSeriviceLocal())
implementation_manager.initialize()

service_reference = TestServiceReference.get_instance()



import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

# app = FastAPI()

# dataframe_name_lookup = {}

# scn_names = []
# scn_ports = []
# list_dataset_id = []
# IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")


# if os.environ.get("IV_FILEPATH") is not None:
#     IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

# with open(IV_SETTINGS_FILE) as initial_settings:
#     configuration = json.load(initial_settings)
#     for entry in configuration["secure_computation_nodes"]:
#         scn_names.append(entry["ip_address"])
#         scn_ports.append(5556)
#         list_dataset_id.append(entry["dataset_id"])


# TODO make this a other implementation that autoconfigures
# participant_service = ParticipantServiceClientDict()
# for dataset_id, scn_name, scn_port in zip(list_dataset_id, scn_names, scn_ports):
#     participant_service.register_client(dataset_id, ClientRPCZero(scn_name, scn_port))
#     print(f"Connected to SCN {scn_name} serving dataset {dataset_id}")


# implementation_manager = ImplementationManager.get_instance()
# implementation_manager.set_participant_service(participant_service)
# implementation_manager.initialize()

# app = FastAPI()

# service_reference = TestServiceReference.get_instance()

# dataframe_name_lookup = {}

# scn_names = []
# scn_ports = []
# list_dataset_id = []
# IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")


# # if os.environ.get("IV_FILEPATH") is not None:
# #     IV_SETTINGS_FILE = os.environ.get("IV_FILEPATH")

# with open(IV_SETTINGS_FILE) as initial_settings:
#     configuration = json.load(initial_settings)
#     for entry in configuration["secure_computation_nodes"]:
#         scn_names.append(entry["ip_address"])
#         scn_ports.append(5556)
#         list_dataset_id.append(entry["dataset_id"])

# implementation_manager = ImplementationManager.get_instance()
# implementation_manager.set_participant_service(ParticipantSeriviceLocal())
# implementation_manager.initialize()


