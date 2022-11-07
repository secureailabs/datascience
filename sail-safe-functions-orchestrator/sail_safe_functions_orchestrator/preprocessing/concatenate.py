from sail_safe_functions.preprocessing.concatenate_precompute import (
    ConcatenatePrecompute,
)
from sail_safe_functions_orchestrator.data_model.data_model_series import (
    DataModelSeries,
)
from sail_safe_functions_orchestrator.series_federated import SeriesFederated
from sail_safe_functions_orchestrator.tools_common import check_instance


def concatenate(
    sample_0: SeriesFederated, sample_1: SeriesFederated
) -> SeriesFederated:
    """
    Function to concatenate SeriesFederated TODO: Needs more information

        :param sample_0: First input series
        :type sample_0: SeriesFederated
        :param sample_1: Second input series
        :type sample_1: SeriesFederated
        :return: concatenated series
        :rtype: series
    """
    return Concatenate.run(sample_0, sample_1)


class Concatenate:
    """Federate wrapper safe function for the pandas concatenate"""

    def run(sample_0: SeriesFederated, sample_1: SeriesFederated):
        """
        Federate wrapper safe function for the pandas concatenate

            :param sample_0: First input series
            :type sample_0: SeriesFederated
            :param sample_1: Second input series
            :type sample_1: SeriesFederated
            :return: concatenated series
            :rtype: series
        """
        check_instance(sample_0, SeriesFederated)
        check_instance(sample_1, SeriesFederated)
        list_reference = []
        series_name = (
            sample_0.series_name + "_" + sample_1.series_name + "_concatinated"
        )
        data_model_series = DataModelSeries.create_numerical(
            series_name, -1, None, DataModelSeries.AgregatorComputed
        )

        for dataset_id in sample_0.list_dataset_id:  # TODO rework abcs
            client = sample_0.service_client.get_client(dataset_id)
            series_0 = sample_0.dict_reference_series[dataset_id]
            series_1 = sample_1.dict_reference_series[dataset_id]
            list_reference.append(
                client.call(
                    ConcatenatePrecompute, series_0, series_1, data_model_series
                )
            )
        return SeriesFederated(
            sample_0.service_client, list_reference, data_model_series
        )
