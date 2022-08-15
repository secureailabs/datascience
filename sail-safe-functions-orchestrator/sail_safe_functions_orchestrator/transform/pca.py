import numpy
from sail_safe_functions_orchestrator.data_frame_federated import DataFrameFederated
from sail_safe_functions_orchestrator.transform.transform_base import TransformBase


class PCA(TransformBase):
    def __init__(self, component_count) -> None:
        self.component_count = component_count
        self.array_mean = None
        self.array_transform = None
        self.array_singular_value = None

    def fit(self, data_frame: DataFrameFederated):
        # TODO maybe this could be improved on doing a actual federated SVD
        # TODO the sklearn implemention worries about conditioning a lot here as well
        # array_source = data_frame.to_numpy()
        array_source = data_frame  # FOT NOW
        self.array_mean = numpy.mean(array_source, axis=0)

        array = array_source - self.array_mean

        array_covaraince = numpy.dot(array.T, array)
        self.array_singular_value, self.array_transform = numpy.linalg.eig(array_covaraince)
        order = numpy.flip(numpy.argsort(self.array_singular_value))  # sorting in normaly implied by doing a SVD
        self.array_singular_value = self.array_singular_value[order]

        self.array_singular_value = numpy.sqrt(self.array_singular_value)
        self.array_transform = self.array_transform.T[order, :]
        self.array_transform = self.flip_sign(self.array_transform).T

        self.array_transform = self.array_transform[:, : self.component_count]
        self.array_singular_value = self.array_singular_value[: self.component_count]

    def transform(self, data_frame: DataFrameFederated) -> DataFrameFederated:
        # array_source = data_frame.to_numpy()
        array_source = data_frame  # FOT NOW
        # array_source -= array_mean

        return numpy.dot(array_source, self.array_transform)

    def flip_sign(self, v):
        # orginaly this is calls flip svd and it is based on U,
        # since we do not do a full SVD and we do not have U we base this on V
        # the result is sometimes differently mirrored compared to sklearn but it is deterministic.

        max_abs_rows = numpy.argmax(numpy.abs(v), axis=1)
        signs = numpy.sign(v[range(v.shape[0]), max_abs_rows])
        v *= signs[:, numpy.newaxis]
        return v
