from typing import List

import numpy as np
import pandas as pd
from sail_safe_functions_orchestrator.data_model.data_model_data_frame import DataModelDataFrame
from sail_safe_functions_orchestrator.data_model.data_model_series import DataModelSeries
from sail_safe_functions.safe_function_base import SafeFunctionBase

class PragmaticNoise(SafeFunctionBase):
    """
    Adds noise to categorical, boolean, numeric and continous columns in a pandas dataframe
    """

    def col_noise_numeric(self, column: pd.Series, col_resolution: float, scale: float) -> pd.Series:
        """
        Adds noise to numeric and continuous columns scaled
        to one standard deviation from the mean.

        :param column: column to be noised
        :type column: pd.Series

        :param col_resolution: The resolution at which numeric noise may be added.
        This makes noised values harder to distinguish.
        This is taken from the scheme accompanying the dataset.
        :type col_resolution: float

        :param scale: Used to scale the amount of noise which may be applied to original values.
        This is intended to be set from 0-1, 1 being the full standard deviation magnitude will be allowed.
        :type col_resolution: float

        :return noised_column: The noised column to be added to the noised dataset
        :type noised_column: pd.Series
        """

        noised_column = column.copy()
        # find std_dev to help us scale our noise addition
        std_dev = noised_column.std()
        # Generate our distribution
        noise = np.random.laplace(0.0, 0.1 * std_dev * scale, 10000)
        # For each row in our column
        for i in range(len(noised_column)):
            # scale noise to the resolution size for this column
            if col_resolution is not None:
                noise[i] = noise[i] - (noise[i] % col_resolution)
            # Add the noise to the column
            noised_column[i] += noise[i]
        return noised_column

    def col_noise_categorical(self, column: pd.Series, list_values: List[str], frequency: float) -> pd.Series:
        """
        Adds noise to categorical columns by swapping categories of elements based
        on frequency of occurence in the column at given intervals.

        :param column: column to be noised
        :type column: pd.Series

        :param list_values: The list of possible values which can be occupied by the column.
        This is taken from the dataset scheme.
        :type list_values: List[str]

        :param frequency: This determines the rate at which we swap categorical values in
        the column. When this is set to 1, 100% of elements will be swapped. If this is 0
        0% of columns will be swapped.
        :type frequency: float

        :return noised_column: The noised column to be added to the noised dataset
        :type noised_column: pd.Series
        """
        noised_column = column.copy()
        # For each row in our column
        for i in range(len(noised_column)):
            # If we are noising this column
            if np.random.uniform(0, 1) <= frequency:
                # For each category in our list of categories
                for cat in list_values:
                    # If our random number (0-1) is les than the probability of this category occuring
                    if np.random.uniform(0, 1) < column.value_counts("normal")[cat]:
                        # switch the category with this value
                        noised_column[i] = cat
                        break
        return noised_column

    def run(
        self,
        dataset: pd.DataFrame,
        data_model: DataModelDataFrame,
        noise_scale: float,
        cat_swap_frequency: float,
    ) -> pd.DataFrame:
        """
        A function which takes a dataset and it's associated schema and churns out a noised version of that dataset.

        :param dataset: This is the original dataset to be noised.
        :type dataset: pd.DataFrame

        :param schema: The schema associated with the original dataset
        :type schema: DataModelDataFrame

        :param noise_scale: This scales the magnitude of noise to be added to numeric values.
        1 is noise of up to 100% of a standard deviation from the column mean.
        :type noise_scale: float

        :param cat_swap_frequency: This determines the rate at which we swap categorical values in
        the column. When this is set to 1, 100% of elements will be swapped. If this is 0
        0% of columns will be swapped.
        :type cat_swap_frequency: float

        :return noised_dataset: The noised version of the original dataset.
        :type noised_dataset: pd.DataFrame
        """
        noised_dataset = dataset.copy()
        for series_name in data_model.list_series_name:
            data_model_series = data_model[series_name]
            if series_name == "classification":
                # print("Skipped Classification Column: "+column)
                continue
            elif data_model_series.type_data_level == DataModelSeries.DataLevelInterval:
                # print("Noising Numeric Column: "+ column)
                noised_dataset[series_name] = self.col_noise_numeric(
                    dataset[series_name],
                    data_model_series.resolution,
                    scale=noise_scale,
                )
            elif data_model_series.type_data_level == DataModelSeries.DataLevelCategorical:
                # print("Noising Categorical Column: "+ column)
                noised_dataset[series_name] = self.col_noise_categorical(
                    dataset[series_name],
                    data_model_series.list_value,
                    frequency=cat_swap_frequency,
                )

        print("Done")
        return noised_dataset
