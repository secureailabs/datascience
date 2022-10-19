import json
import os
import shutil
import tempfile
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import pandas
from sail_safe_functions_orchestrator.data_model_tabular import \
    DataModelTabular
from sail_safe_functions_orchestrator.dataset_tabular import DatasetTabular
from sail_safe_functions_orchestrator.packager_dataset.serializer_dataset_base import \
    SerializerDatasetBase


class SerializerDatasetCsvv1(SerializerDatasetBase):
    # A general note on the ZipFile package: The initializer of ZipFile takes a fourth argument called allowZip64.
    # It’s a Boolean argument that tells ZipFile to create ZIP files with the .zip64 extension for files larger than 4 GB.

    # zipfile.ZIP_DEFLATED	Deflate	zlib
    # zipfile.ZIP_BZIP2	    Bzip2	bz2
    # zipfile.ZIP_LZMA	    LZMA	lzma
    def __init__(self) -> None:
        super().__init__("csvv1")

    def read_dataset(self, path_dirdataset_id) -> DatasetTabular:
        pass

    def read_dataset_for_path(self, path_dir_dataset_source) -> DatasetTabular:
        # TODO check signature
        with ZipFile(path_dir_dataset_source) as zip_file_dataset:

            path_file_dataset_header = "dataset_header.json"
            path_file_data_model = "data_model.zip"
            path_file_data_content = "data_content.zip"
            header_dataset = json.loads(zip_file_dataset.read(path_file_dataset_header))
            # TODO check header

            data_model = DataModelTabular.from_json(json.loads(zip_file_dataset.read(path_file_data_model)))
            dict_table = {}
            with ZipFile(BytesIO(zip_file_dataset.read(path_file_data_content))) as zip_file_data_content:
                for name_file in zip_file_data_content.namelist():
                    if not name_file.endswith(".csv"):
                        raise Exception()
                    dict_table[name_file[:4]] = pandas.read_csv(zip_file_data_content.read(name_file))
            return DatasetTabular(data_model, dict_table)

    def write_dataset_tabular(self, path_file_dataset_target, dataset_tabular: DatasetTabular) -> None:
        path_dir_temp = tempfile.mkdtemp()
        path_file_dataset_header_temp = os.path.join(path_dir_temp, "dataset_header.json")
        path_file_data_model_temp = os.path.join(path_dir_temp, "data_model.json")
        path_file_data_content_temp = os.path.join(path_dir_temp, "data_content.zip")

        # write dataset header
        header_dataset = {}
        header_dataset["data_federation_id"] = ""  # TODOdataset_tabular.dataset_id
        header_dataset["dataset_id"] = ""  # TODO dataset_tabular.dataset_id
        with open(path_file_dataset_header_temp, "w") as file:
            json.dump(header_dataset, file)

        # write data model
        with open(path_file_data_model_temp, "w") as file:
            json.dump(file, dataset_tabular.data_model.to_json())

        # write data content
        with ZipFile(path_file_data_content_temp, "w", ZIP_DEFLATED) as zip_file_dataset:
            for table_id, data_frame in dataset_tabular.dict_table.items():
                # saving a data frame to a buffer (same as with a regular file):
                buffer = BytesIO()
                data_frame.to_csv(buffer)
                # write buffer to zip
                name_file = table_id + ".csv"
                zip_file_dataset.write(buffer, arcname=name_file)
        # TODO do data_content encryption here

        with ZipFile(path_file_dataset_target, "w", ZIP_DEFLATED) as archive:
            archive.write(path_file_dataset_header_temp, arcname="dataset_header.json")
            archive.write(path_file_data_model_temp, arcname="data_model.json")
            archive.write(path_file_data_content_temp, arcname="data_content.zip")

        # TODO sign the resulting dataset with some signature to prevent tampering
        shutil.rmtree(path_dir_temp)
        # TODO potential security hazard when this does not get removed: solution do all of this in memory
