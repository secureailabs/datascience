from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions.aggregator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions.aggregator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions.aggregator.service_reference import ServiceReference
from sail_safe_functions.safe_function_base import SafeFunctionBase


class ConvertToDatasetTabularPrecompute(SafeFunctionBase):
    # TODO this might be in the wrong spot, is this a convert function?
    @staticmethod
    def run(
        reference_dataset_logitudinal: ReferenceDatasetLongitudinal,
        dataset_federation_id: str,
        dataset_federation_name: str,
        dataset_id: str,
        dataset_name: str,
        data_model_tabular: DataModelTabular,
    ) -> ReferenceDatasetTabular:
        check_instance(reference_dataset_logitudinal, ReferenceDatasetLongitudinal)
        check_instance(dataset_federation_id, str)
        check_instance(dataset_federation_name, str)
        check_instance(dataset_id, str)
        check_instance(dataset_name, str)
        check_instance(data_model_tabular, DataModelTabular)

        dataset_logitudinal = ServiceReference.get_instance().reference_to_dataset_longitudinal(
            reference_dataset_logitudinal
        )
        dataset_tabular = dataset_logitudinal.convert_to_dataset_tabular(
            dataset_federation_id, dataset_federation_name, dataset_id, dataset_name, data_model_tabular
        )
        return ServiceReference.get_instance().dataset_tabular_to_reference(dataset_tabular)
