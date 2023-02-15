import plotly.graph_objects as go
from sail_aggregator_client.models import BodyHistogram, BodyKernelDensityEstimation
from sail_aggregator_client.sail_class import SyncOperations
from plotly.graph_objects import Figure



def histogram(operation: SyncOperations, series_1_id: str, bin_count: int) -> Figure:
    """
    Performs the federated histogram.
    It take on federated series and bin count. Returns the histogram.
    -----------
        :param operation: Object used to reference sail_aggregator_client function calls
        :type operation: SyncOperations
        :param series_1_id: The id of the series being visualised
        :type series_1_id: string
        :param bin_count: The second sample of data
        :type bin_count: int
        :return: pyplot figure valuie
        :rtype: pyplot object

    it works to segregate the range into several bins and then returns the number
    of instances in each bin. This function is used to build the histogram.

    A histogram is an approximate representation of the distribution of numerical data.
    The term was first introduced by Karl Pearson.[1] To construct a histogram, the first step
    is to "bin" (or "bucket") the range of values—that is, divide the entire range of values
    into a series of intervals—and then count how many values fall into each interval.
    The bins are usually specified as consecutive, non-overlapping intervals of a variable.
    The bins (intervals) must be adjacent and are often (but not required to be) of equal size.[2]

    If the bins are of equal size, a rectangle is erected over the bin with height proportional to
    the frequency—the number of cases in each bin. A histogram may also be normalized to display
    "relative" frequencies. It then shows the proportion of cases that fall into each of several
    categories, with the sum of the heights equaling 1.
    -----------

    Example
    -----------
    >>> from sail_safe_functions.aggregator.visualization.histogram_federated import HistogramFederate
    >>> values = HistogramFederate.Run(sample_0,5)

    Example-2
    --------
    Look into thte notebook

    https://github.com/secureailabs/ScratchPad/blob/master/Saurabh/demo_histogram.ipynb

    It will show you the result in the plot.

    """
    body = BodyHistogram(series_1_id, bin_count)
    result = operation.histogram(body).additional_properties["figure"]

    return go.Figure(result)


def kernel_density_estimation(operation: SyncOperations, series_1_id: str, bin_size: float) -> Figure:
    """
    Performs the federated kernel density estimation.
    It take on federated series and bin count. Returns the kde plot.
    -----------
        :param operation: Object used to reference sail_aggregator_client function calls
        :type operation: SyncOperations
        :param series_1_id: The id of the series being visualised
        :type series_1_id: string
        :param bin_size: The size of each bin to sort the histogram into
        :type bin_size: float
        :return: pyplot figure
        :rtype: pyplot object

    """
    body = BodyKernelDensityEstimation(series_1_id, bin_size)
    result = operation.kernel_density_estimation(body).additional_properties["figure"]

    return go.Figure(result)
