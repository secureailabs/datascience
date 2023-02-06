import plotly.graph_objects as go
from fast_api_client.models import BodyVisualizationHistogram, BodyVisualizationKernelDensityEstimation


def histogram(operation, series_1_id, bin_count):

    body = BodyVisualizationHistogram(series_1_id, bin_count)
    result = operation.visualization_histogram(body).additional_properties["figure"]

    return result


# TODO: Fix whatever caused the repeated name
def kernel_density_estimation(operation, series_1_id: str, bin_size: float):

    body = BodyVisualizationKernelDensityEstimation(series_1_id, bin_size)
    result = operation.visualization_kernel_density_estimation(body).additional_properties["figure"]

    return result
