from sail_core.api.participant_service_base import ParticipantServiceBase


class ParticipantSeriviceLocal(ParticipantServiceBase):
    def call(self, dataset_id: str, safe_function_class, *argument_list, **argument_dict):
        return safe_function_class.run(*argument_list, **argument_dict)

    def initialize(self) -> None:
        pass
