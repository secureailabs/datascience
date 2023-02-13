from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...models.mean_response_mean import MeanResponseMean
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: str,
) -> Dict[str, Any]:
    url = "{}/statistics/mean".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body

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
) -> Optional[Union[HTTPValidationError, MeanResponseMean]]:

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = MeanResponseMean.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, MeanResponseMean]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: str,
) -> Response[Union[HTTPValidationError, MeanResponseMean]]:
    """Mean

     Computes the Mean of a Series.

    Args:
        json_body (str): The identifer of the Series to be computed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, MeanResponseMean]]
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
    json_body: str,
) -> Optional[Union[HTTPValidationError, MeanResponseMean]]:
    """Mean

     Computes the Mean of a Series.

    Args:
        json_body (str): The identifer of the Series to be computed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, MeanResponseMean]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: str,
) -> Response[Union[HTTPValidationError, MeanResponseMean]]:
    """Mean

     Computes the Mean of a Series.

    Args:
        json_body (str): The identifer of the Series to be computed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, MeanResponseMean]]
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
    json_body: str,
) -> Optional[Union[HTTPValidationError, MeanResponseMean]]:
    """Mean

     Computes the Mean of a Series.

    Args:
        json_body (str): The identifer of the Series to be computed.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, MeanResponseMean]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
