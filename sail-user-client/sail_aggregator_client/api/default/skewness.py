from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.skewness_response_skewness import SkewnessResponseSkewness
from ...types import UNSET, Response


def _get_kwargs(
    *,
    client: Client,
    series_id: str,
) -> Dict[str, Any]:
    url = "{}/statistics/skewness".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["series_id"] = series_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Union[HTTPValidationError, SkewnessResponseSkewness]]:

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = SkewnessResponseSkewness.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, SkewnessResponseSkewness]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    series_id: str,
) -> Response[Union[HTTPValidationError, SkewnessResponseSkewness]]:
    """Skewness

     Computes the Skewness of a Series.

    Args:
        series_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SkewnessResponseSkewness]]
    """

    kwargs = _get_kwargs(
        client=client,
        series_id=series_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    series_id: str,
) -> Optional[Union[HTTPValidationError, SkewnessResponseSkewness]]:
    """Skewness

     Computes the Skewness of a Series.

    Args:
        series_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SkewnessResponseSkewness]]
    """

    return sync_detailed(
        client=client,
        series_id=series_id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    series_id: str,
) -> Response[Union[HTTPValidationError, SkewnessResponseSkewness]]:
    """Skewness

     Computes the Skewness of a Series.

    Args:
        series_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SkewnessResponseSkewness]]
    """

    kwargs = _get_kwargs(
        client=client,
        series_id=series_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    series_id: str,
) -> Optional[Union[HTTPValidationError, SkewnessResponseSkewness]]:
    """Skewness

     Computes the Skewness of a Series.

    Args:
        series_id (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, SkewnessResponseSkewness]]
    """

    return (
        await asyncio_detailed(
            client=client,
            series_id=series_id,
        )
    ).parsed
