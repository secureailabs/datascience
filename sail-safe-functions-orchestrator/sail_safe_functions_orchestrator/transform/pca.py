from typing import List

import numpy
from sail_safe_functions_orchestrator import statistics, transform
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.transform.transform_base import TransformBase


class PCA(TransformBase):
    def __init__(self, component_count) -> None:
        self.component_count = component_count
        self.array_mean = None
        self.array_transform = None
        self.array_singular_value = None

    def fit(self, data_frame: DataFrameFederated, list_name_feature: List[str]) -> None:
        # TODO maybe this could be improved on doing a actual federated SVD
        # TODO the sklearn implemention worries about conditioning a lot here as well: future work

        list_mean = []
        for name_feature in data_frame.columns:
            list_mean.append(statistics.mean(data_frame[name_feature]))
        self.array_mean = numpy.array(list_mean)  # TODO this we might not need

        array_covaraince = statistics.covariance_matrix(data_frame)
        self.array_singular_value, self.array_transform = numpy.linalg.eig(array_covaraince)
        order = numpy.flip(numpy.argsort(self.array_singular_value))  # sorting in normaly implied by doing a SVD
        self.array_singular_value = self.array_singular_value[order]

        self.array_singular_value = numpy.sqrt(self.array_singular_value)  # TODO this might have to go
        self.array_transform = self.array_transform.T[order, :]  # TODO double transpose
        self.array_transform = self.flip_sign(
            self.array_transform
        ).T  # TODO double transpose: we can change the flip function

        self.array_transform = self.array_transform[:, : self.component_count]
        self.array_singular_value = self.array_singular_value[: self.component_count]

    def transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:

        # array_source -= array_mean TODO do we really not need this?
        list_name_feature_target = [f"component_{i}" for i in range(self.component_count)]
        array_add = numpy.zeros(self.array_transform.shape[0])
        return transform.linear(
            data_frame, array_add, self.array_transform, data_frame.columns, list_name_feature_target
        )

    def flip_sign(self, v) -> numpy.ndarray:
        # orginaly this is calls flip svd and it is based on U,
        # since we do not do a full SVD and we do not have U we base this on V
        # the result is sometimes differently mirrored compared to sklearn but it is deterministic.

        max_abs_rows = numpy.argmax(numpy.abs(v), axis=1)
        signs = numpy.sign(v[range(v.shape[0]), max_abs_rows])
        v *= signs[:, numpy.newaxis]
        return v
