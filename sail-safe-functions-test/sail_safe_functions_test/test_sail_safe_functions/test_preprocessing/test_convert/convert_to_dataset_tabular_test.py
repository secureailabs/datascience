import pytest
from sail_safe_functions_orchestrator import preprocessing, statistics
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions_orchestrator.data_model.data_model_tabular import DataModelTabular
from sail_safe_functions_orchestrator.dataset_longitudinal_federated import DatasetLongitudinalFederated
from sail_safe_functions_orchestrator.dataset_tabular_federated import DatasetTabularFederated
from sail_safe_functions_orchestrator.preprocessing import convert
from sail_safe_functions_orchestrator.series_federated import SeriesFederated


@pytest.mark.active
def test_convert_to_dataset_tabular(dataset_longitudinal_r4sep2019_20_1: DatasetLongitudinalFederated):
    """
    This test our ability to convert a longitudinal dataset to a tabular one
    """
    dataset_longitudinal = dataset_longitudinal_r4sep2019_20_1

    # Arrange
    dataset_federation_id = "a892f738-4f6f-11ed-bdc3-0242ac120002"
    dataset_federation_name = "r4sep2019_csvv1_20_1"
    data_frame_name = "data_frame_0"

    data_model_data_frame = DataModelDataFrame(data_frame_name)
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_mean",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalMean,
            unit="kg/m2",
        )
    )
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_first",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalFirstOccurance,
            unit="kg/m2",
        )
    )

    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_last",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalLastOccurance,
            unit="kg/m2",
        )
    )
    data_model_tablular = DataModelTabular()
    data_model_tablular.add_data_model_data_frame(data_model_data_frame)

    # act
    dataset_tabular = convert.convert_to_dataset_tabular(
        dataset_longitudinal, dataset_federation_id, dataset_federation_name, data_model_tablular
    )

    name_series_1 = dataset_tabular[data_frame_name].list_series_name[1]
    name_series_2 = dataset_tabular[data_frame_name].list_series_name[2]
    data_model_series = dataset_tabular[data_frame_name][name_series_1].data_model_series
    series_1 = dataset_tabular[data_frame_name][name_series_1]
    series_2 = dataset_tabular[data_frame_name][name_series_2]
    mean_1 = statistics.mean(series_1)
    mean_2 = statistics.mean(series_2)

    # assert
    assert isinstance(dataset_tabular, DatasetTabularFederated)
    assert isinstance(dataset_tabular[data_frame_name], DataFrameFederated)
    assert isinstance(dataset_tabular[data_frame_name][name_series_1], SeriesFederated)
    assert data_model_series.type_data_level == DataModelSeries.DataLevelInterval
    assert data_model_series.unit == "kg/m2"
    assert 21.342993316312352 == mean_1
    assert 24.493595595296163 == mean_2


@pytest.mark.active
def test_convert_to_dataset_tabular_t_test(dataset_longitudinal_r4sep2019_20_1: DatasetLongitudinalFederated):
    """
    This test our ability to convert a longitudinal dataset to a tabular one and do a t-test
    """
    dataset_longitudinal = dataset_longitudinal_r4sep2019_20_1

    # Arrange
    dataset_federation_id = "a892f738-4f6f-11ed-bdc3-0242ac120002"
    dataset_federation_name = "r4sep2019_csvv1_20_1"
    data_frame_name = "data_frame_0"

    data_model_data_frame = DataModelDataFrame(data_frame_name)
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_mean",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalMean,
            unit="kg/m2",
        )
    )
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_first",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalFirstOccurance,
            unit="kg/m2",
        )
    )

    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_last",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalLastOccurance,
            unit="kg/m2",
        )
    )
    data_model_tablular = DataModelTabular()
    data_model_tablular.add_data_model_data_frame(data_model_data_frame)

    # act
    dataset_tabular = convert.convert_to_dataset_tabular(
        dataset_longitudinal, dataset_federation_id, dataset_federation_name, data_model_tablular
    )
    name_series_1 = dataset_tabular[data_frame_name].list_series_name[1]
    name_series_2 = dataset_tabular[data_frame_name].list_series_name[2]
    data_model_series = dataset_tabular[data_frame_name][name_series_1].data_model_series
    series_1 = dataset_tabular[data_frame_name][name_series_1]
    series_2 = dataset_tabular[data_frame_name][name_series_2]
    t_statistic, p_value = statistics.student_t_test(series_1, series_2, "less")

    # assert
    assert isinstance(dataset_tabular, DatasetTabularFederated)
    assert isinstance(dataset_tabular[data_frame_name], DataFrameFederated)
    assert isinstance(dataset_tabular[data_frame_name][name_series_1], SeriesFederated)
    assert DataModelSeries.DataLevelInterval == data_model_series.type_data_level
    assert "kg/m2" == data_model_series.unit
    assert -1.7486887374051483 == t_statistic
    assert 0.0442098972205117 == p_value


@pytest.mark.active
def test_convert_to_dataset_tabular_many_procedure(dataset_longitudinal_r4sep2019_20_1: DatasetLongitudinalFederated):
    """
    This test our ability to convert a longitudinal dataset to a tabular and do a varriety of procedures, 
    we are not so much intrested in the results but more if they dont raise do raise any exeptions
    """
    dataset_longitudinal = dataset_longitudinal_r4sep2019_20_1

    # Arrange
    dataset_federation_id = "a892f738-4f6f-11ed-bdc3-0242ac120002"
    dataset_federation_name = "r4sep2019_csvv1_20_1"
    data_frame_name = "data_frame_0"

    data_model_data_frame = DataModelDataFrame(data_frame_name)
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_mean",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalMean,
            unit="kg/m2",
        )
    )
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_first",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalFirstOccurance,
            unit="kg/m2",
        )
    )

    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_last",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalLastOccurance,
            unit="kg/m2",
        )
    )
    data_model_tablular = DataModelTabular()
    data_model_tablular.add_data_model_data_frame(data_model_data_frame)

    # act
    dataset_tabular = convert.convert_to_dataset_tabular(
        dataset_longitudinal, dataset_federation_id, dataset_federation_name, data_model_tablular
    )
    name_series_1 = dataset_tabular[data_frame_name].list_series_name[1]
    name_series_2 = dataset_tabular[data_frame_name].list_series_name[2]
    series_1 = dataset_tabular[data_frame_name][name_series_1]
    series_2 = dataset_tabular[data_frame_name][name_series_2]
    statistics.count(series_1)
    statistics.mean(series_1)
    statistics.variance(series_1)
    statistics.skewness(series_1)
    statistics.kurtosis(series_1)
    statistics.min_max(series_1)
    #statistics.levene_test(series_1, series_2) #TODO broken
    statistics.pearson(series_1, series_2, "less")
    statistics.spearman(series_1, series_2, "less", "cdf")


    statistics.student_t_test(series_1, series_2, "less")
    statistics.welch_t_test(series_1, series_2, "less")
    statistics.paired_t_test(series_1, series_2, "less")


@pytest.mark.slow
def test_convert_to_dataset_tabular_big(dataset_longitudinal_r4sep2019_1k_3: DatasetLongitudinalFederated):
    """
    This test our ability to convert a longitudinal dataset to a tabular one
    """
    dataset_longitudinal = dataset_longitudinal_r4sep2019_1k_3

    # Arrange
    dataset_federation_id = "a892f738-4f6f-11ed-bdc3-0242ac120002"
    dataset_federation_name = "r4sep2019_csvv1_20_1"
    data_frame_name = "data_frame_0"

    data_model_data_frame = DataModelDataFrame(data_frame_name)
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_mean",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalMean,
            unit="kg/m2",
        )
    )
    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_first",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalFirstOccurance,
            unit="kg/m2",
        )
    )

    data_model_data_frame.add_data_model_series(
        DataModelSeries.create_numerical(
            series_name="bmi_last",
            measurement_source_name="Observation:Body Mass Index",
            type_agregator=DataModelSeries.AgregatorIntervalLastOccurance,
            unit="kg/m2",
        )
    )
    data_model_tablular = DataModelTabular()
    data_model_tablular.add_data_model_data_frame(data_model_data_frame)

    # act
    dataset_tabular = convert.convert_to_dataset_tabular(
        dataset_longitudinal, dataset_federation_id, dataset_federation_name, data_model_tablular
    )

    data_frame_nonan = preprocessing.drop_missing(
        dataset_tabular[data_frame_name], axis=0, how="any", thresh=None, subset=None
    )
    name_series_1 = data_frame_nonan.list_series_name[1]
    name_series_2 = data_frame_nonan.list_series_name[2]
    data_model_series = data_frame_nonan[name_series_1].data_model_series
    series_1 = data_frame_nonan[name_series_1]
    series_2 = data_frame_nonan[name_series_2]
    mean_1 = statistics.mean(series_1)
    mean_2 = statistics.mean(series_2)
    t_statistic, p_value = statistics.student_t_test(series_1, series_2, "less")

    # assert
    assert isinstance(dataset_tabular, DatasetTabularFederated)
    assert isinstance(data_frame_nonan, DataFrameFederated)
    assert isinstance(data_frame_nonan[name_series_1], SeriesFederated)
    assert data_model_series.type_data_level == DataModelSeries.DataLevelInterval
    assert data_model_series.unit == "kg/m2"
    assert 24.97839070020774 == mean_1
    assert 26.14043993190191 == mean_2

    assert -2.5605551123530965 == t_statistic
    assert 0.00536218929892478 == p_value
