import json
import os
import shutil
import tempfile
from typing import Dict
from zipfile import ZIP_DEFLATED, ZipFile


class ToolsDatasetPackaging:
    def fhirv1_validate_data_federation_header(data_federation_id: str, data_federation_header: Dict) -> bool:
        if data_federation_header["data_federation_type"] != "fhirv1":
            raise Exception("incorrect data_federation_type")
        if data_federation_header["data_federation_id"] != data_federation_id:
            data_federation_id_found = data_federation_header["data_federation_id"]
            raise Exception(
                f"iconsitent data_federation_id expected: {data_federation_id} found {data_federation_id_found}"
            )
        return True

    def fhirv1_validate_dataset_header(data_federation_id: str, dataset_id: str, dataset_header: Dict) -> bool:
        if dataset_header["data_federation_type"] != "fhirv1":
            raise Exception("incorrect data_federation_type")
        if dataset_header["data_federation_id"] != data_federation_id:
            data_federation_id_found = dataset_header["data_federation_id"]
            raise Exception(
                f"iconsitent data_federation_id expected: {data_federation_id} found {data_federation_id_found}"
            )
        if dataset_header["dataset_id"] != dataset_id:
            dataset_id_found = dataset_header["dataset_id"]
            raise Exception(f"iconsitent data_federation_id expected: {dataset_id} found {dataset_id_found}")
        # TODO check keys
        return True

    def fhirv1_package_data_federation(
        path_dir_data_federation_unpackaged: str, path_dir_data_federation_packaged: str, data_federation_id: str
    ) -> None:

        path_dir_data_federation_root = os.path.join(path_dir_data_federation_unpackaged, data_federation_id)
        if not os.path.isdir(path_dir_data_federation_root):
            raise Exception(f"no such data federation  at: {path_dir_data_federation_root}")

        path_file_data_federation_packaged = os.path.join(
            path_dir_data_federation_packaged, data_federation_id + ".zip"
        )
        if os.path.isfile(path_file_data_federation_packaged):
            raise Exception(f"data federation already packaged at: {path_file_data_federation_packaged}")

        path_file_data_federation_header = os.path.join(path_dir_data_federation_root, "data_federation_header.json")
        if not os.path.isfile(path_file_data_federation_header):
            raise Exception(f"missing data_federation_header at: {path_file_data_federation_header}")

        with open(path_file_data_federation_header, "r") as file:
            data_federation_header = json.load(file)
        if not ToolsDatasetPackaging.fhirv1_validate_data_federation_header(data_federation_id, data_federation_header):
            raise Exception(f"invalid data_federation_header at: {path_file_data_federation_header}")

        # TODO validate
        path_dir_dataset_root = os.path.join(path_dir_data_federation_root, "dataset")
        if not os.path.isdir(path_dir_dataset_root):
            raise Exception(f"missing dataset_root at: {path_dir_data_federation_root}")

        list_name_dataset_id = os.listdir(path_dir_dataset_root)
        path_dir_dataset_root_temp = tempfile.mkdtemp()

        # package every dataset in the data federation in a temp dir
        for dataset_id in list_name_dataset_id:
            path_dir_dataset = os.path.join(path_dir_dataset_root, dataset_id)
            path_file_dataset = os.path.join(path_dir_dataset_root_temp, dataset_id + ".zip")
            ToolsDatasetPackaging.fhirv1_package_dataset(
                data_federation_id, dataset_id, path_dir_dataset, path_file_dataset
            )

        # zip entire dataset
        with ZipFile(path_file_data_federation_packaged, "w", ZIP_DEFLATED, compresslevel=9) as archive:
            # add header
            archive.write(path_file_data_federation_header, arcname="dataset_header.json")
            # add data_set
            for name_file in os.listdir(path_dir_dataset_root_temp):
                path_file_source = os.path.join(path_dir_dataset_root_temp, name_file)
                path_file_target = os.path.join("dataset", name_file)
                archive.write(path_file_source, arcname=path_file_target)

        # remove the temp dir where everything was packaged
        shutil.rmtree(path_dir_dataset_root_temp)

    def fhirv1_package_dataset(data_federation_id, dataset_id, path_dir_dataset, path_file_target) -> None:
        path_file_dataset_header = os.path.join(path_dir_dataset, "dataset_header.json")
        if not os.path.isfile(path_file_dataset_header):
            raise Exception(f"missing dataset_header at: {path_file_dataset_header}")

        path_dir_data_content = os.path.join(path_dir_dataset, "data_content")
        if not os.path.isdir(path_dir_data_content):
            raise Exception(f"missing data_content at: {path_dir_data_content}")

        if 0 == len(os.listdir(path_dir_data_content)):
            raise Exception(f"data_content empty at: {path_dir_data_content}")

        path_dir_data_model = os.path.join(path_dir_dataset, "data_model")
        if not os.path.isdir(path_dir_data_model):
            raise Exception(f"missing data_model at: {path_dir_data_model}")

        if 0 == len(os.listdir(path_dir_data_model)):
            raise Exception(f"data_model empty at: {path_dir_data_model}")

        with open(path_file_dataset_header, "r") as file:
            dataset_header = json.load(file)

        if not ToolsDatasetPackaging.fhirv1_validate_dataset_header(data_federation_id, dataset_id, dataset_header):
            raise Exception(f"invalid data_federation_header at: {path_file_dataset_header}")

        # TODO validate data_model

        # TODO validate data_content using data_model

        # if the content file exist delete to avoid duplicate addition and such
        path_file_data_content_zip = os.path.join(path_dir_dataset, "data_content.zip")
        if os.path.isfile(path_file_data_content_zip):
            os.remove(path_file_data_content_zip)

        # zip and compress content
        with ZipFile(path_file_data_content_zip, "w", ZIP_DEFLATED, compresslevel=9) as archive:
            for name_file in os.listdir(path_dir_data_content):
                path_file = os.path.join(path_dir_data_content, name_file)
                archive.write(path_file, arcname=name_file)

        # TODO encrypt data_content

        # zip entire dataset
        with ZipFile(path_file_target, "w", ZIP_DEFLATED, compresslevel=9) as archive:
            # add header
            #
            archive.write(path_file_dataset_header, arcname="dataset_header.json")
            archive.write(path_file_data_content_zip, arcname="data_content.zip")
            # NOTE it is a bit inconsitent that the content is zipped but the data model is not
            # This is because the content might need to be encrypted and the data model should be
            # plaintext in the packaged form. There is something to be said for giving the datamodel
            # its own whole format when we revisit this
            for name_file in os.listdir(path_dir_data_model):
                path_file = os.path.join(path_dir_data_model, name_file)
                archive.write(path_file, arcname=path_file)

        # remove
        os.remove(path_file_data_content_zip)


# Note: The initializer of ZipFile takes a fourth argument called allowZip64.
# It’s a Boolean argument that tells ZipFile to create ZIP files with the .zip64 extension for files larger than 4 GB.

# zipfile.ZIP_DEFLATED	Deflate	zlib
# zipfile.ZIP_BZIP2	Bzip2	bz2
# zipfile.ZIP_LZMA	LZMA	lzma
