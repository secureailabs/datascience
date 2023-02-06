from .api.default import (
    data_frame_query,
    data_frame_select_series,
    data_frame_tabular_select_dataframe,
    dataframe_drop_missing,
    dataframe_model_add_new_series_model,
    dataset_tabular_fhirv1,
    mann_whitney_u_test,
    new_data_model_data_frame,
    new_series_model_numerical,
    new_tabular_model,
    read_dataset_tabular_from_longitudinal,
    read_longitudinal_fhirv1,
    read_tabular_dataframe_csvv1,
    statistics_chisquare,
    statistics_count,
    statistics_kolmogorov_smirnov_test,
    statistics_kurtosis,
    statistics_levene_test,
    statistics_mean,
    statistics_min_max,
    statistics_paired_t_test,
    statistics_pearson,
    statistics_skewness,
    statistics_spearman,
    statistics_student_t_test,
    statistics_variance,
    statistics_welch_t_test,
    statistics_wilcoxon_signed_rank_test,
    tabular_model_add_dataframe_model,
    visualization_histogram,
    visualization_kernel_density_estimation,
)
from .client import AuthenticatedClient, Client
from .models.body_data_frame_query import BodyDataFrameQuery
from .models.body_data_frame_select_series import BodyDataFrameSelectSeries
from .models.body_data_frame_tabular_select_dataframe import BodyDataFrameTabularSelectDataframe
from .models.body_dataframe_model_add_new_series_model import BodyDataframeModelAddNewSeriesModel
from .models.body_dataset_tabular_fhirv_1 import BodyDatasetTabularFhirv1
from .models.body_mann_whitney_u_test import BodyMannWhitneyUTest
from .models.body_new_series_model_numerical import BodyNewSeriesModelNumerical
from .models.body_read_dataset_tabular_from_longitudinal import BodyReadDatasetTabularFromLongitudinal
from .models.body_statistics_chisquare import BodyStatisticsChisquare
from .models.body_statistics_kolmogorov_smirnov_test import BodyStatisticsKolmogorovSmirnovTest
from .models.body_statistics_levene_test import BodyStatisticsLeveneTest
from .models.body_statistics_paired_t_test import BodyStatisticsPairedTTest
from .models.body_statistics_pearson import BodyStatisticsPearson
from .models.body_statistics_spearman import BodyStatisticsSpearman
from .models.body_statistics_student_t_test import BodyStatisticsStudentTTest
from .models.body_statistics_welch_t_test import BodyStatisticsWelchTTest
from .models.body_statistics_wilcoxon_signed_rank_test import BodyStatisticsWilcoxonSignedRankTest
from .models.body_tabular_model_add_dataframe_model import BodyTabularModelAddDataframeModel
from .models.body_visualization_histogram import BodyVisualizationHistogram
from .models.body_visualization_kernel_density_estimation import BodyVisualizationKernelDensityEstimation
from .models.data_federation import DataFederation
from .models.data_frame_query_response_data_frame_query import DataFrameQueryResponseDataFrameQuery
from .models.data_frame_select_series_response_data_frame_select_series import (
    DataFrameSelectSeriesResponseDataFrameSelectSeries,
)
from .models.data_frame_tabular_select_dataframe_response_data_frame_tabular_select_dataframe import (
    DataFrameTabularSelectDataframeResponseDataFrameTabularSelectDataframe,
)
from .models.dataframe_drop_missing_response_dataframe_drop_missing import (
    DataframeDropMissingResponseDataframeDropMissing,
)
from .models.dataframe_model_add_new_series_model_response_dataframe_model_add_new_series_model import (
    DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel,
)
from .models.dataset_tabular_fhirv_1_response_dataset_tabular_fhirv_1 import (
    DatasetTabularFhirv1ResponseDatasetTabularFhirv1,
)
from .models.mann_whitney_u_test_response_mann_whitney_u_test import MannWhitneyUTestResponseMannWhitneyUTest
from .models.new_data_model_data_frame_response_new_data_model_data_frame import (
    NewDataModelDataFrameResponseNewDataModelDataFrame,
)
from .models.new_series_model_numerical_response_new_series_model_numerical import (
    NewSeriesModelNumericalResponseNewSeriesModelNumerical,
)
from .models.new_tabular_model_response_new_tabular_model import NewTabularModelResponseNewTabularModel
from .models.read_dataset_tabular_from_longitudinal_response_read_dataset_tabular_from_longitudinal import (
    ReadDatasetTabularFromLongitudinalResponseReadDatasetTabularFromLongitudinal,
)
from .models.read_longitudinal_fhirv_1_response_read_longitudinal_fhirv_1 import (
    ReadLongitudinalFhirv1ResponseReadLongitudinalFhirv1,
)
from .models.read_tabular_dataframe_csvv_1_response_read_tabular_dataframe_csvv_1 import (
    ReadTabularDataframeCsvv1ResponseReadTabularDataframeCsvv1,
)
from .models.statistics_chisquare_response_statistics_chisquare import StatisticsChisquareResponseStatisticsChisquare
from .models.statistics_count_response_statistics_count import StatisticsCountResponseStatisticsCount
from .models.statistics_kolmogorov_smirnov_test_response_statistics_kolmogorov_smirnov_test import (
    StatisticsKolmogorovSmirnovTestResponseStatisticsKolmogorovSmirnovTest,
)
from .models.statistics_kurtosis_response_statistics_kurtosis import StatisticsKurtosisResponseStatisticsKurtosis
from .models.statistics_levene_test_response_statistics_levene_test import (
    StatisticsLeveneTestResponseStatisticsLeveneTest,
)
from .models.statistics_mean_response_statistics_mean import StatisticsMeanResponseStatisticsMean
from .models.statistics_min_max_response_statistics_min_max import StatisticsMinMaxResponseStatisticsMinMax
from .models.statistics_paired_t_test_response_statistics_paired_t_test import (
    StatisticsPairedTTestResponseStatisticsPairedTTest,
)
from .models.statistics_pearson_response_statistics_pearson import StatisticsPearsonResponseStatisticsPearson
from .models.statistics_skewness_response_statistics_skewness import StatisticsSkewnessResponseStatisticsSkewness
from .models.statistics_spearman_response_statistics_spearman import StatisticsSpearmanResponseStatisticsSpearman
from .models.statistics_student_t_test_response_statistics_student_t_test import (
    StatisticsStudentTTestResponseStatisticsStudentTTest,
)
from .models.statistics_variance_response_statistics_variance import StatisticsVarianceResponseStatisticsVariance
from .models.statistics_welch_t_test_response_statistics_welch_t_test import (
    StatisticsWelchTTestResponseStatisticsWelchTTest,
)
from .models.statistics_wilcoxon_signed_rank_test_response_statistics_wilcoxon_signed_rank_test import (
    StatisticsWilcoxonSignedRankTestResponseStatisticsWilcoxonSignedRankTest,
)
from .models.tabular_model_add_dataframe_model_response_tabular_model_add_dataframe_model import (
    TabularModelAddDataframeModelResponseTabularModelAddDataframeModel,
)
from .models.visualization_histogram_response_visualization_histogram import (
    VisualizationHistogramResponseVisualizationHistogram,
)
from .models.visualization_kernel_density_estimation_response_visualization_kernel_density_estimation import (
    VisualizationKernelDensityEstimationResponseVisualizationKernelDensityEstimation,
)


class SyncAuthenticatedOperations:
    def __init__(self, client: AuthenticatedClient) -> None:
        self._client = client


class SyncOperations:
    def __init__(self, client: Client) -> None:
        self._client = client

    def new_tabular_model(
        self,
    ) -> NewTabularModelResponseNewTabularModel:
        """New Data Frame Tabular

         Create new Tabular Data Model

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[NewTabularModelResponseNewTabularModel]
        """

        response = new_tabular_model.sync(
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, NewTabularModelResponseNewTabularModel)
        return response

    def new_series_model_numerical(
        self,
        json_body: BodyNewSeriesModelNumerical,
    ) -> NewSeriesModelNumericalResponseNewSeriesModelNumerical:
        """New Series Model Numerical

         Create new numerical Series Model

        Args:
            json_body (BodyNewSeriesModelNumerical):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[NewSeriesModelNumericalResponseNewSeriesModelNumerical]
        """

        response = new_series_model_numerical.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, NewSeriesModelNumericalResponseNewSeriesModelNumerical)
        return response

    def tabular_model_add_dataframe_model(
        self,
        json_body: BodyTabularModelAddDataframeModel,
    ) -> TabularModelAddDataframeModelResponseTabularModelAddDataframeModel:
        """Tabular Model Add Dataframe Model

         Add a Dataframe model to a Tabular Dataframe Model

        Args:
            json_body (BodyTabularModelAddDataframeModel):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[TabularModelAddDataframeModelResponseTabularModelAddDataframeModel]
        """

        response = tabular_model_add_dataframe_model.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, TabularModelAddDataframeModelResponseTabularModelAddDataframeModel)
        return response

    def new_data_model_data_frame(
        self,
        json_body: str,
    ) -> NewDataModelDataFrameResponseNewDataModelDataFrame:
        """New Data Model Data Frame

         Create a new Dataframe model.

        Args:
            json_body (str): Desired name of the new Dataframe

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[NewDataModelDataFrameResponseNewDataModelDataFrame]
        """

        response = new_data_model_data_frame.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, NewDataModelDataFrameResponseNewDataModelDataFrame)
        return response

    def dataframe_model_add_new_series_model(
        self,
        json_body: BodyDataframeModelAddNewSeriesModel,
    ) -> DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel:
        """Dataframe Model Add Series Model

         Create a new numerical series model and add it to a Dataframe model.

        Args:
            json_body (BodyDataframeModelAddNewSeriesModel):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel]
        """

        response = dataframe_model_add_new_series_model.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel)
        return response

    def read_longitudinal_fhirv1(
        self,
    ) -> ReadLongitudinalFhirv1ResponseReadLongitudinalFhirv1:
        """Read Longitudinal Fhirv1

         Reads a Longitudinal dataset from a fhirv1 data source.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ReadLongitudinalFhirv1ResponseReadLongitudinalFhirv1]
        """

        response = read_longitudinal_fhirv1.sync(
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, ReadLongitudinalFhirv1ResponseReadLongitudinalFhirv1)
        return response

    def read_dataset_tabular_from_longitudinal(
        self,
        json_body: BodyReadDatasetTabularFromLongitudinal,
    ) -> ReadDatasetTabularFromLongitudinalResponseReadDatasetTabularFromLongitudinal:
        """Read Dataset Tabular From Longitudinal

         Populates a Tabular dataset from a Longitudinal dataset.

        Args:
            json_body (BodyReadDatasetTabularFromLongitudinal):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ReadDatasetTabularFromLongitudinalResponseReadDatasetTabularFromLongitudinal]
        """

        response = read_dataset_tabular_from_longitudinal.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, ReadDatasetTabularFromLongitudinalResponseReadDatasetTabularFromLongitudinal)
        return response

    def dataset_tabular_fhirv1(
        self,
        json_body: BodyDatasetTabularFhirv1,
    ) -> DatasetTabularFhirv1ResponseDatasetTabularFhirv1:
        """Dataset Tabular Fhirv1

         Pull data from fhirv1 source straight to tabular Dataframe.

        Args:
            json_body (BodyDatasetTabularFhirv1):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[DatasetTabularFhirv1ResponseDatasetTabularFhirv1]
        """

        response = dataset_tabular_fhirv1.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, DatasetTabularFhirv1ResponseDatasetTabularFhirv1)
        return response

    def read_tabular_dataframe_csvv1(
        self,
        json_body: DataFederation,
    ) -> ReadTabularDataframeCsvv1ResponseReadTabularDataframeCsvv1:
        """Read Tabular Dataframe Csvv1

         Pull a Tabular Dataframe from csvv1 source.

        Args:
            json_body (DataFederation): TODO: What is this datatype? This should be a reference

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ReadTabularDataframeCsvv1ResponseReadTabularDataframeCsvv1]
        """

        response = read_tabular_dataframe_csvv1.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, ReadTabularDataframeCsvv1ResponseReadTabularDataframeCsvv1)
        return response

    def data_frame_tabular_select_dataframe(
        self,
        json_body: BodyDataFrameTabularSelectDataframe,
    ) -> DataFrameTabularSelectDataframeResponseDataFrameTabularSelectDataframe:
        """Data Frame Tabular Select Dataframe

         Select an individual datafame from a tabular dataframe.

        Args:
            json_body (BodyDataFrameTabularSelectDataframe):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[DataFrameTabularSelectDataframeResponseDataFrameTabularSelectDataframe]
        """

        response = data_frame_tabular_select_dataframe.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, DataFrameTabularSelectDataframeResponseDataFrameTabularSelectDataframe)
        return response

    def data_frame_select_series(
        self,
        json_body: BodyDataFrameSelectSeries,
    ) -> DataFrameSelectSeriesResponseDataFrameSelectSeries:
        """Data Frame Select Series

         Select an individual series from a  dataframe.

        Args:
            json_body (BodyDataFrameSelectSeries):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[DataFrameSelectSeriesResponseDataFrameSelectSeries]
        """

        response = data_frame_select_series.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, DataFrameSelectSeriesResponseDataFrameSelectSeries)
        return response

    def dataframe_drop_missing(
        self,
        json_body: str,
    ) -> DataframeDropMissingResponseDataframeDropMissing:
        """Dataframe Drop Missing

         Drop all missing values from a dataframe and return this copy.

        Args:
            json_body (str): Identifier of the dataframe to be cleaned.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[DataframeDropMissingResponseDataframeDropMissing]
        """

        response = dataframe_drop_missing.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, DataframeDropMissingResponseDataframeDropMissing)
        return response

    def data_frame_query(
        self,
        json_body: BodyDataFrameQuery,
    ) -> DataFrameQueryResponseDataFrameQuery:
        """Data Frame Query

         Query a Dataframe for a given String.

        Args:
            json_body (BodyDataFrameQuery):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[DataFrameQueryResponseDataFrameQuery]
        """

        response = data_frame_query.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, DataFrameQueryResponseDataFrameQuery)
        return response

    def statistics_chisquare(
        self,
        json_body: BodyStatisticsChisquare,
    ) -> StatisticsChisquareResponseStatisticsChisquare:
        """Statistics Chisquare

         Computes the chisquare of two Series.

        Args:
            json_body (BodyStatisticsChisquare):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsChisquareResponseStatisticsChisquare]
        """

        response = statistics_chisquare.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsChisquareResponseStatisticsChisquare)
        return response

    def statistics_count(
        self,
        json_body: str,
    ) -> StatisticsCountResponseStatisticsCount:
        """Count

         Computes the count of a Series.

        Args:
            json_body (str): The identifier of the series to be counted.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsCountResponseStatisticsCount]
        """

        response = statistics_count.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsCountResponseStatisticsCount)
        return response

    def statistics_kolmogorov_smirnov_test(
        self,
        json_body: BodyStatisticsKolmogorovSmirnovTest,
    ) -> StatisticsKolmogorovSmirnovTestResponseStatisticsKolmogorovSmirnovTest:
        """Kolmogorov Smirnov Test

         Computes Kolmogorov Smirnov Test of a Series.

        Args:
            json_body (BodyStatisticsKolmogorovSmirnovTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsKolmogorovSmirnovTestResponseStatisticsKolmogorovSmirnovTest]
        """

        response = statistics_kolmogorov_smirnov_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsKolmogorovSmirnovTestResponseStatisticsKolmogorovSmirnovTest)
        return response

    def statistics_kurtosis(
        self,
        series_id: str,
    ) -> StatisticsKurtosisResponseStatisticsKurtosis:
        """Kurtosis

         Computes Kurtosis of a Series.

        Args:
            series_id (str):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsKurtosisResponseStatisticsKurtosis]
        """

        response = statistics_kurtosis.sync(
            client=self._client,
            series_id=series_id,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsKurtosisResponseStatisticsKurtosis)
        return response

    def statistics_levene_test(
        self,
        json_body: BodyStatisticsLeveneTest,
    ) -> StatisticsLeveneTestResponseStatisticsLeveneTest:
        """Levene Test

         Computes the Levene Test of two Series.

        Args:
            json_body (BodyStatisticsLeveneTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsLeveneTestResponseStatisticsLeveneTest]
        """

        response = statistics_levene_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsLeveneTestResponseStatisticsLeveneTest)
        return response

    def mann_whitney_u_test(
        self,
        json_body: BodyMannWhitneyUTest,
    ) -> MannWhitneyUTestResponseMannWhitneyUTest:
        """Mann Whitney U Test

         Computes the Mann Whitney U Test of two Series.

        Args:
            json_body (BodyMannWhitneyUTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[MannWhitneyUTestResponseMannWhitneyUTest]
        """

        response = mann_whitney_u_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, MannWhitneyUTestResponseMannWhitneyUTest)
        return response

    def statistics_mean(
        self,
        json_body: str,
    ) -> StatisticsMeanResponseStatisticsMean:
        """Mean

         Computes the Mean of a Series.

        Args:
            json_body (str): The identifer of the Series to be computed.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsMeanResponseStatisticsMean]
        """

        response = statistics_mean.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsMeanResponseStatisticsMean)
        return response

    def statistics_min_max(
        self,
        json_body: str,
    ) -> StatisticsMinMaxResponseStatisticsMinMax:
        """Min Max

         Computes the Min and Max of a Series.

        Args:
            json_body (str): The identifer of the Series to be computed.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsMinMaxResponseStatisticsMinMax]
        """

        response = statistics_min_max.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsMinMaxResponseStatisticsMinMax)
        return response

    def statistics_paired_t_test(
        self,
        json_body: BodyStatisticsPairedTTest,
    ) -> StatisticsPairedTTestResponseStatisticsPairedTTest:
        """Paired T Test

         Computes the Paired T Test of two Series.

        Args:
            json_body (BodyStatisticsPairedTTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsPairedTTestResponseStatisticsPairedTTest]
        """

        response = statistics_paired_t_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsPairedTTestResponseStatisticsPairedTTest)
        return response

    def statistics_pearson(
        self,
        json_body: BodyStatisticsPearson,
    ) -> StatisticsPearsonResponseStatisticsPearson:
        """Pearson

         Computes the Pearson of two Series.

        Args:
            json_body (BodyStatisticsPearson):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsPearsonResponseStatisticsPearson]
        """

        response = statistics_pearson.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsPearsonResponseStatisticsPearson)
        return response

    def statistics_skewness(
        self,
        series_id: str,
    ) -> StatisticsSkewnessResponseStatisticsSkewness:
        """Skewness

         Computes the Skewness of a Series.

        Args:
            series_id (str):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsSkewnessResponseStatisticsSkewness]
        """

        response = statistics_skewness.sync(
            client=self._client,
            series_id=series_id,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsSkewnessResponseStatisticsSkewness)
        return response

    def statistics_spearman(
        self,
        json_body: BodyStatisticsSpearman,
    ) -> StatisticsSpearmanResponseStatisticsSpearman:
        """Spearman

         Computes the Spearman statistic of two Series.

        Args:
            json_body (BodyStatisticsSpearman):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsSpearmanResponseStatisticsSpearman]
        """

        response = statistics_spearman.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsSpearmanResponseStatisticsSpearman)
        return response

    def statistics_student_t_test(
        self,
        json_body: BodyStatisticsStudentTTest,
    ) -> StatisticsStudentTTestResponseStatisticsStudentTTest:
        """Student T Test

         Computes the Student T test of two Series.

        Args:
            json_body (BodyStatisticsStudentTTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsStudentTTestResponseStatisticsStudentTTest]
        """

        response = statistics_student_t_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsStudentTTestResponseStatisticsStudentTTest)
        return response

    def statistics_variance(
        self,
        json_body: str,
    ) -> StatisticsVarianceResponseStatisticsVariance:
        """Variance

         Computes the Variance of a Series.

        Args:
            json_body (str): The identifier of the series

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsVarianceResponseStatisticsVariance]
        """

        response = statistics_variance.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsVarianceResponseStatisticsVariance)
        return response

    def statistics_welch_t_test(
        self,
        json_body: BodyStatisticsWelchTTest,
    ) -> StatisticsWelchTTestResponseStatisticsWelchTTest:
        """Welch T Test

         Computes the Welch T test of two Series.

        Args:
            json_body (BodyStatisticsWelchTTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsWelchTTestResponseStatisticsWelchTTest]
        """

        response = statistics_welch_t_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsWelchTTestResponseStatisticsWelchTTest)
        return response

    def statistics_wilcoxon_signed_rank_test(
        self,
        json_body: BodyStatisticsWilcoxonSignedRankTest,
    ) -> StatisticsWilcoxonSignedRankTestResponseStatisticsWilcoxonSignedRankTest:
        """Wilcoxon Signed Rank Test

         Computes the Wilcoxon signed rank test of two Series.

        Args:
            json_body (BodyStatisticsWilcoxonSignedRankTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StatisticsWilcoxonSignedRankTestResponseStatisticsWilcoxonSignedRankTest]
        """

        response = statistics_wilcoxon_signed_rank_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StatisticsWilcoxonSignedRankTestResponseStatisticsWilcoxonSignedRankTest)
        return response

    def visualization_histogram(
        self,
        json_body: BodyVisualizationHistogram,
    ) -> VisualizationHistogramResponseVisualizationHistogram:
        """Histogram Federated

         Creates a histogram of a given Series.

        Args:
            json_body (BodyVisualizationHistogram):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[VisualizationHistogramResponseVisualizationHistogram]
        """

        response = visualization_histogram.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, VisualizationHistogramResponseVisualizationHistogram)
        return response

    def visualization_kernel_density_estimation(
        self,
        json_body: BodyVisualizationKernelDensityEstimation,
    ) -> VisualizationKernelDensityEstimationResponseVisualizationKernelDensityEstimation:
        """Kernel Density Estimation

         Creates a Kernel Density Estimation of a given Series.

        Args:
            json_body (BodyVisualizationKernelDensityEstimation):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[VisualizationKernelDensityEstimationResponseVisualizationKernelDensityEstimation]
        """

        response = visualization_kernel_density_estimation.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, VisualizationKernelDensityEstimationResponseVisualizationKernelDensityEstimation)
        return response
