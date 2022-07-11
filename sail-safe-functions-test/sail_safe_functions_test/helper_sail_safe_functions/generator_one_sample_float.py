from random import uniform
from typing import List

import numpy
import pandas
from sail_safe_functions_test.helper_sail_safe_functions.series_federated_local import SeriesFederatedLocal


class GeneratorOneSampleFloat:
    def __init__(
        self,
        name: str,
        type_distribution: str,
        mean: float,
        standard_deviation: float,
        list_weight_federation: List[float],
        resolution: float,
    ) -> None:

        if not type_distribution in ["normal", "uniform"]:
            raise ValueError()
        self.name = name
        self.type_distribution = type_distribution
        self.mean = mean
        self.standard_deviation = standard_deviation
        self.list_weight_federation = list_weight_federation

        self.resolution = resolution

    def generate(self, size_sample):
        sample_0 = SeriesFederatedLocal()
        for i, weight_federation in enumerate(self.list_weight_federation):
            count_federation = int(round(size_sample * weight_federation))
            if self.type_distribution == "normal":
                array_0 = numpy.random.normal(self.mean, self.standard_deviation, count_federation)

            elif self.type_distribution == "uniform":
                shift = self.standard_deviation * (numpy.sqrt(12) / 2)
                array_0 = numpy.random.uniform(self.mean - shift, self.mean + shift, count_federation)

            if not self.resolution == -1:
                array_0 = (array_0 * (1 / self.resolution)).round().astype(int) * self.resolution
            sample_0.add_series(
                f"federation_{i}",
                pandas.Series(array_0),
            )

        return sample_0
