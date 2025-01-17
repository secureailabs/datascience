import uuid

from sail_core.tools_common import check_instance
from sail_safe_functions.aggregator.data_frame import DataFrame
from sail_safe_functions.aggregator.dataset_longitudinal import DatasetLongitudinal
from sail_safe_functions.aggregator.dataset_tabular import DatasetTabular
from sail_safe_functions.aggregator.reference_data_frame import ReferenceDataFrame
from sail_safe_functions.aggregator.reference_dataset_longitudinal import ReferenceDatasetLongitudinal
from sail_safe_functions.aggregator.reference_dataset_tabular import ReferenceDatasetTabular
from sail_safe_functions.aggregator.reference_series import ReferenceSeries
from sail_safe_functions.aggregator.series import Series


class ServiceReference:
    def __init__(self) -> None:
        self.dict_reference = {}

        # TODO split the referencer into different types?
        # (or allow set guids for the computgrah)

        # TODO all the references could be merged because we are not using the datamodel anyway

    def __call__(self):
        raise TypeError("Singletons must be accessed through `get_instance()`.")

    @staticmethod
    def get_instance() -> "ServiceReference":
        try:
            return ServiceReference._instance

        except AttributeError:
            ServiceReference._instance = ServiceReference()
            return ServiceReference._instance

    def generate_reference_id(self) -> str:
        return str(uuid.uuid4())

    ###
    def dataset_longitudinal_to_reference(
        self, dataset_longitudinal: DatasetLongitudinal
    ) -> ReferenceDatasetLongitudinal:
        check_instance(dataset_longitudinal, DatasetLongitudinal)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = dataset_longitudinal
        return ReferenceDatasetLongitudinal(
            dataset_longitudinal.dataset_id,
            reference_id,
            dataset_longitudinal.data_model,
        )

    def reference_to_dataset_longitudinal(
        self,
        reference: ReferenceDatasetLongitudinal,
    ) -> DatasetLongitudinal:
        check_instance(reference, ReferenceDatasetLongitudinal)
        if reference.reference_id not in self.dict_reference:
            raise ValueError(f"Dataset not loaded: {reference.reference_id}")
        return self.dict_reference[reference.reference_id]

    ###
    def dataset_tabular_to_reference(self, dataset_tabular: DatasetTabular) -> ReferenceDatasetTabular:
        check_instance(dataset_tabular, DatasetTabular)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = dataset_tabular
        return ReferenceDatasetTabular(dataset_tabular.dataset_id, reference_id, dataset_tabular.data_model)

    def reference_to_dataset_tabular(
        self,
        reference: ReferenceDatasetTabular,
    ) -> DatasetTabular:
        check_instance(reference, ReferenceDatasetTabular)
        if reference.reference_id not in self.dict_reference:
            raise ValueError(f"Dataset not loaded: {reference.reference_id}")
        return self.dict_reference[reference.reference_id]

    ###

    def data_frame_to_reference(self, data_frame: DataFrame) -> ReferenceDataFrame:
        check_instance(data_frame, DataFrame)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = data_frame
        return ReferenceDataFrame(data_frame.dataset_id, reference_id, data_frame.data_model_data_frame)

    def reference_to_data_frame(
        self,
        reference: ReferenceDataFrame,
    ) -> DataFrame:
        check_instance(reference, ReferenceDataFrame)
        if reference.reference_id not in self.dict_reference:
            raise ValueError(f"DataFrame not loaded: {reference.reference_id}")
        return self.dict_reference[reference.reference_id]

    ###
    def series_to_reference(self, series: Series) -> ReferenceSeries:
        check_instance(series, Series)
        reference_id = self.generate_reference_id()
        self.dict_reference[reference_id] = series
        return ReferenceSeries(series.dataset_id, reference_id, series.data_model_series)

    def reference_to_series(
        self,
        reference: ReferenceSeries,
    ) -> Series:
        check_instance(reference, ReferenceSeries)
        if reference.reference_id not in self.dict_reference:
            raise ValueError(f"DataFrame not loaded: {reference.reference_id}")
        return self.dict_reference[reference.reference_id]
