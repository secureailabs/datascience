from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import Client
from ...models.body_kernel_density_estimation import BodyKernelDensityEstimation
from ...models.http_validation_error import HTTPValidationError
from ...models.kernel_density_estimation_response_kernel_density_estimation import (
    KernelDensityEstimationResponseKernelDensityEstimation,
)
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: BodyKernelDensityEstimation,
) -> Dict[str, Any]:
    url = "{}/visualisation/kernel_density_estimation".format(client.base_url)

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
) -> Optional[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]:

    if response.status_code < 200 or response.status_code >= 300:
        raise Exception(f"Failure status code: {response.status_code}. Details: {response.text}")

    if response.status_code == HTTPStatus.OK:
        response_200 = KernelDensityEstimationResponseKernelDensityEstimation.from_dict(response.json())

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
) -> Response[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: BodyKernelDensityEstimation,
) -> Response[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]:
    """Kernel Density Estimation

     Creates a Kernel Density Estimation of a given Series.

    Args:
        json_body (BodyKernelDensityEstimation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]
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
    json_body: BodyKernelDensityEstimation,
) -> Optional[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]:
    """Kernel Density Estimation

     Creates a Kernel Density Estimation of a given Series.

    Args:
        json_body (BodyKernelDensityEstimation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: BodyKernelDensityEstimation,
) -> Response[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]:
    """Kernel Density Estimation

     Creates a Kernel Density Estimation of a given Series.

    Args:
        json_body (BodyKernelDensityEstimation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]
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
    json_body: BodyKernelDensityEstimation,
) -> Optional[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]:
    """Kernel Density Estimation

     Creates a Kernel Density Estimation of a given Series.

    Args:
        json_body (BodyKernelDensityEstimation):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, KernelDensityEstimationResponseKernelDensityEstimation]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
