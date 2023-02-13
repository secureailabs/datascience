from sail_safe_functions.test.helper_sail_safe_functions.participant_service_local import ParticipantSeriviceLocal
from sail_safe_functions.test.helper_sail_safe_functions.test_service_reference import TestServiceReference
from sail_core.implementation.participant_service_client_dict import ParticipantServiceClientDict
from sail_core.implementation_manager import ImplementationManager
from routers import data_model, data_ingestion, data_manipulation, preprocessing, statistics, visualization
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Response, status

from fastapi import FastAPI

app = FastAPI()

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

@app.get(
    path="/",
    description="landing page",
    response_description="simple string.",
    response_model=dict,
    response_model_by_alias=False,
    response_model_exclude_unset=True,
    dependencies=None,
    status_code=status.HTTP_200_OK,
    operation_id="landing",
)
def home():
    return {"message":"hello world home page"}


import uvicorn

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


