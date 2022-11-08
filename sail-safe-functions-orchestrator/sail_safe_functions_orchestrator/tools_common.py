from sail_safe_functions_orchestrator.series import Series


def check_instance(instance, class_check) -> None:
    if not isinstance(instance, class_check):
        raise Exception(f"{instance} is not instance of class: {class_check} instead type is {type(instance)}")


def check_series_nan(series: Series) -> None:
    if 0 < series.isna().sum():
        raise Exception(f"series {series.series_name} cannot containt nan or None values")


def check_empty_series(series: Series) -> None:
    if series.size == 0:
        raise Exception("series cannot be empty")


def check_series_one_value(series: Series) -> None:
    if series.size == 2:
        raise Exception(f"series {series.series_name} cannot containt only one value")
