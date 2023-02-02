from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.body_dataframe_model_add_new_series_model import BodyDataframeModelAddNewSeriesModel
from ...models.dataframe_model_add_new_series_model_response_dataframe_model_add_new_series_model import (
    DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel,
)
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: BodyDataframeModelAddNewSeriesModel,
) -> Dict[str, Any]:
    url = "{}/dataframe_model_add_new_series_model.".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]:

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: BodyDataframeModelAddNewSeriesModel,
) -> Response[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]:
    """Dataframe Model Add Series Model

     Create a new numerical series model and add it to a Dataframe model.

    Args:
        json_body (BodyDataframeModelAddNewSeriesModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    json_body: BodyDataframeModelAddNewSeriesModel,
) -> Optional[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]:
    """Dataframe Model Add Series Model

     Create a new numerical series model and add it to a Dataframe model.

    Args:
        json_body (BodyDataframeModelAddNewSeriesModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: BodyDataframeModelAddNewSeriesModel,
) -> Response[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]:
    """Dataframe Model Add Series Model

     Create a new numerical series model and add it to a Dataframe model.

    Args:
        json_body (BodyDataframeModelAddNewSeriesModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    json_body: BodyDataframeModelAddNewSeriesModel,
) -> Optional[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]:
    """Dataframe Model Add Series Model

     Create a new numerical series model and add it to a Dataframe model.

    Args:
        json_body (BodyDataframeModelAddNewSeriesModel):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DataframeModelAddNewSeriesModelResponseDataframeModelAddNewSeriesModel, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
