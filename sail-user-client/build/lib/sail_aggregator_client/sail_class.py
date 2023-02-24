from .api.default import (
    chisquare,
    count,
    data_frame_query,
    data_frame_select_series,
    data_frame_tabular_select_dataframe,
    dataframe_drop_missing,
    dataframe_model_add_new_series_model,
    dataset_tabular_fhirv1,
    histogram,
    kernel_density_estimation,
    kolmogorov_smirnov_test,
    kurtosis,
    landing,
    levene_test,
    mann_whitney_u_test,
    mean,
    min_max,
    new_data_model_data_frame,
    new_series_model_numerical,
    new_tabular_model,
    paired_t_test,
    pearson,
    read_dataset_tabular_from_longitudinal,
    read_longitudinal_fhirv1,
    read_tabular_dataframe_csvv1,
    skewness,
    spearman,
    student_t_test,
    tabular_model_add_dataframe_model,
    variance,
    welch_t_test,
    wilcoxon_signed_rank_test,
)
from .client import AuthenticatedClient, Client
from .models.body_chisquare import BodyChisquare
from .models.body_data_frame_query import BodyDataFrameQuery
from .models.body_data_frame_select_series import BodyDataFrameSelectSeries
from .models.body_data_frame_tabular_select_dataframe import BodyDataFrameTabularSelectDataframe
from .models.body_dataframe_model_add_new_series_model import BodyDataframeModelAddNewSeriesModel
from .models.body_dataset_tabular_fhirv_1 import BodyDatasetTabularFhirv1
from .models.body_histogram import BodyHistogram
from .models.body_kernel_density_estimation import BodyKernelDensityEstimation
from .models.body_kolmogorov_smirnov_test import BodyKolmogorovSmirnovTest
from .models.body_levene_test import BodyLeveneTest
from .models.body_mann_whitney_u_test import BodyMannWhitneyUTest
from .models.body_new_series_model_numerical import BodyNewSeriesModelNumerical
from .models.body_paired_t_test import BodyPairedTTest
from .models.body_pearson import BodyPearson
from .models.body_read_dataset_tabular_from_longitudinal import BodyReadDatasetTabularFromLongitudinal
from .models.body_spearman import BodySpearman
from .models.body_student_t_test import BodyStudentTTest
from .models.body_tabular_model_add_dataframe_model import BodyTabularModelAddDataframeModel
from .models.body_welch_t_test import BodyWelchTTest
from .models.body_wilcoxon_signed_rank_test import BodyWilcoxonSignedRankTest
from .models.chisquare_response_chisquare import ChisquareResponseChisquare
from .models.count_response_count import CountResponseCount
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
from .models.histogram_response_histogram import HistogramResponseHistogram
from .models.kernel_density_estimation_response_kernel_density_estimation import (
    KernelDensityEstimationResponseKernelDensityEstimation,
)
from .models.kolmogorov_smirnov_test_response_kolmogorov_smirnov_test import (
    KolmogorovSmirnovTestResponseKolmogorovSmirnovTest,
)
from .models.kurtosis_response_kurtosis import KurtosisResponseKurtosis
from .models.landing_response_landing import LandingResponseLanding
from .models.levene_test_response_levene_test import LeveneTestResponseLeveneTest
from .models.mann_whitney_u_test_response_mann_whitney_u_test import MannWhitneyUTestResponseMannWhitneyUTest
from .models.mean_response_mean import MeanResponseMean
from .models.min_max_response_min_max import MinMaxResponseMinMax
from .models.new_data_model_data_frame_response_new_data_model_data_frame import (
    NewDataModelDataFrameResponseNewDataModelDataFrame,
)
from .models.new_series_model_numerical_response_new_series_model_numerical import (
    NewSeriesModelNumericalResponseNewSeriesModelNumerical,
)
from .models.new_tabular_model_response_new_tabular_model import NewTabularModelResponseNewTabularModel
from .models.paired_t_test_response_paired_t_test import PairedTTestResponsePairedTTest
from .models.pearson_response_pearson import PearsonResponsePearson
from .models.read_dataset_tabular_from_longitudinal_response_read_dataset_tabular_from_longitudinal import (
    ReadDatasetTabularFromLongitudinalResponseReadDatasetTabularFromLongitudinal,
)
from .models.read_longitudinal_fhirv_1_response_read_longitudinal_fhirv_1 import (
    ReadLongitudinalFhirv1ResponseReadLongitudinalFhirv1,
)
from .models.read_tabular_dataframe_csvv_1_response_read_tabular_dataframe_csvv_1 import (
    ReadTabularDataframeCsvv1ResponseReadTabularDataframeCsvv1,
)
from .models.skewness_response_skewness import SkewnessResponseSkewness
from .models.spearman_response_spearman import SpearmanResponseSpearman
from .models.student_t_test_response_student_t_test import StudentTTestResponseStudentTTest
from .models.tabular_model_add_dataframe_model_response_tabular_model_add_dataframe_model import (
    TabularModelAddDataframeModelResponseTabularModelAddDataframeModel,
)
from .models.variance_response_variance import VarianceResponseVariance
from .models.welch_t_test_response_welch_t_test import WelchTTestResponseWelchTTest
from .models.wilcoxon_signed_rank_test_response_wilcoxon_signed_rank_test import (
    WilcoxonSignedRankTestResponseWilcoxonSignedRankTest,
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

    def chisquare(
        self,
        json_body: BodyChisquare,
    ) -> ChisquareResponseChisquare:
        """Chisquare

         Computes the chisquare of two Series.

        Args:
            json_body (BodyChisquare):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[ChisquareResponseChisquare]
        """

        response = chisquare.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, ChisquareResponseChisquare)
        return response

    def count(
        self,
        json_body: str,
    ) -> CountResponseCount:
        """Count

         Computes the count of a Series.

        Args:
            json_body (str): The identifier of the series to be counted.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[CountResponseCount]
        """

        response = count.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, CountResponseCount)
        return response

    def kolmogorov_smirnov_test(
        self,
        json_body: BodyKolmogorovSmirnovTest,
    ) -> KolmogorovSmirnovTestResponseKolmogorovSmirnovTest:
        """Kolmogorov Smirnov Test

         Computes Kolmogorov Smirnov Test of a Series.

        Args:
            json_body (BodyKolmogorovSmirnovTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[KolmogorovSmirnovTestResponseKolmogorovSmirnovTest]
        """

        response = kolmogorov_smirnov_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, KolmogorovSmirnovTestResponseKolmogorovSmirnovTest)
        return response

    def kurtosis(
        self,
        series_id: str,
    ) -> KurtosisResponseKurtosis:
        """Kurtosis

         Computes Kurtosis of a Series.

        Args:
            series_id (str):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[KurtosisResponseKurtosis]
        """

        response = kurtosis.sync(
            client=self._client,
            series_id=series_id,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, KurtosisResponseKurtosis)
        return response

    def levene_test(
        self,
        json_body: BodyLeveneTest,
    ) -> LeveneTestResponseLeveneTest:
        """Levene Test

         Computes the Levene Test of two Series.

        Args:
            json_body (BodyLeveneTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[LeveneTestResponseLeveneTest]
        """

        response = levene_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, LeveneTestResponseLeveneTest)
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

    def mean(
        self,
        json_body: str,
    ) -> MeanResponseMean:
        """Mean

         Computes the Mean of a Series.

        Args:
            json_body (str): The identifer of the Series to be computed.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[MeanResponseMean]
        """

        response = mean.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, MeanResponseMean)
        return response

    def min_max(
        self,
        json_body: str,
    ) -> MinMaxResponseMinMax:
        """Min Max

         Computes the Min and Max of a Series.

        Args:
            json_body (str): The identifer of the Series to be computed.

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[MinMaxResponseMinMax]
        """

        response = min_max.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, MinMaxResponseMinMax)
        return response

    def paired_t_test(
        self,
        json_body: BodyPairedTTest,
    ) -> PairedTTestResponsePairedTTest:
        """Paired T Test

         Computes the Paired T Test of two Series.

        Args:
            json_body (BodyPairedTTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[PairedTTestResponsePairedTTest]
        """

        response = paired_t_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, PairedTTestResponsePairedTTest)
        return response

    def pearson(
        self,
        json_body: BodyPearson,
    ) -> PearsonResponsePearson:
        """Pearson

         Computes the Pearson of two Series.

        Args:
            json_body (BodyPearson):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[PearsonResponsePearson]
        """

        response = pearson.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, PearsonResponsePearson)
        return response

    def skewness(
        self,
        series_id: str,
    ) -> SkewnessResponseSkewness:
        """Skewness

         Computes the Skewness of a Series.

        Args:
            series_id (str):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[SkewnessResponseSkewness]
        """

        response = skewness.sync(
            client=self._client,
            series_id=series_id,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, SkewnessResponseSkewness)
        return response

    def spearman(
        self,
        json_body: BodySpearman,
    ) -> SpearmanResponseSpearman:
        """Spearman

         Computes the Spearman statistic of two Series.

        Args:
            json_body (BodySpearman):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[SpearmanResponseSpearman]
        """

        response = spearman.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, SpearmanResponseSpearman)
        return response

    def student_t_test(
        self,
        json_body: BodyStudentTTest,
    ) -> StudentTTestResponseStudentTTest:
        """Student T Test

         Computes the Student T test of two Series.

        Args:
            json_body (BodyStudentTTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[StudentTTestResponseStudentTTest]
        """

        response = student_t_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, StudentTTestResponseStudentTTest)
        return response

    def variance(
        self,
        json_body: str,
    ) -> VarianceResponseVariance:
        """Variance

         Computes the Variance of a Series.

        Args:
            json_body (str): The identifier of the series

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[VarianceResponseVariance]
        """

        response = variance.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, VarianceResponseVariance)
        return response

    def welch_t_test(
        self,
        json_body: BodyWelchTTest,
    ) -> WelchTTestResponseWelchTTest:
        """Welch T Test

         Computes the Welch T test of two Series.

        Args:
            json_body (BodyWelchTTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[WelchTTestResponseWelchTTest]
        """

        response = welch_t_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, WelchTTestResponseWelchTTest)
        return response

    def wilcoxon_signed_rank_test(
        self,
        json_body: BodyWilcoxonSignedRankTest,
    ) -> WilcoxonSignedRankTestResponseWilcoxonSignedRankTest:
        """Wilcoxon Signed Rank Test

         Computes the Wilcoxon signed rank test of two Series.

        Args:
            json_body (BodyWilcoxonSignedRankTest):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[WilcoxonSignedRankTestResponseWilcoxonSignedRankTest]
        """

        response = wilcoxon_signed_rank_test.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, WilcoxonSignedRankTestResponseWilcoxonSignedRankTest)
        return response

    def histogram(
        self,
        json_body: BodyHistogram,
    ) -> HistogramResponseHistogram:
        """Histogram Federated

         Creates a histogram of a given Series.

        Args:
            json_body (BodyHistogram):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[HistogramResponseHistogram]
        """

        response = histogram.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, HistogramResponseHistogram)
        return response

    def kernel_density_estimation(
        self,
        json_body: BodyKernelDensityEstimation,
    ) -> KernelDensityEstimationResponseKernelDensityEstimation:
        """Kernel Density Estimation

         Creates a Kernel Density Estimation of a given Series.

        Args:
            json_body (BodyKernelDensityEstimation):

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[KernelDensityEstimationResponseKernelDensityEstimation]
        """

        response = kernel_density_estimation.sync(
            client=self._client,
            json_body=json_body,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, KernelDensityEstimationResponseKernelDensityEstimation)
        return response

    def landing(
        self,
    ) -> LandingResponseLanding:
        """Home

         landing page

        Raises:
            errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
            httpx.TimeoutException: If the request takes longer than Client.timeout.

        Returns:
            Response[LandingResponseLanding]
        """

        response = landing.sync(
            client=self._client,
        )

        if response is None:
            raise Exception("No response")

        assert isinstance(response, LandingResponseLanding)
        return response
