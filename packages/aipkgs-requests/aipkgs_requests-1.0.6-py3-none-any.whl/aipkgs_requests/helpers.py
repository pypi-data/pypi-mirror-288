import os
import requests
import json


def generic_request(
    method: str,
    url: str,
    headers: dict = None,
    params: dict = None,
    payload: dict = None,
    response_as_json: bool = None,
):
    all_params = {
        "method": method,
        "url": url,
        "headers": headers,
        "params": params,
        "data": (
            json.dumps(payload)
            if isinstance(payload, dict)
            else payload if payload else None
        ),
    }
    not_none_params = {k: v for k, v in all_params.items() if v is not None}
    
    try:
        response = requests.request(**not_none_params)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error
    except requests.exceptions.TooManyRedirects as error:
        raise error
    except requests.ConnectionError as error:
        raise error
    except requests.Timeout as error:
        raise error

    return response.json() if response_as_json else response


# region methods
# region requests
def get_request(url: str, headers: dict = None, params=None, payload=None, res_as_json: bool = None):
    url = url
    payload = payload
    headers = headers

    return generic_request(method="GET", url=url, headers=headers, params=params, payload=payload, response_as_json=res_as_json)


def post_request(url: str, headers: dict = None, params=None, payload=None, res_as_json: bool = None):
    url = url
    payload = payload
    headers = headers

    return generic_request(method="POST", url=url, headers=headers, params=params, payload=payload, response_as_json=res_as_json)


def put_request(url: str, headers: dict = None, params=None, payload=None, res_as_json: bool = None):
    url = url
    payload = payload
    headers = headers

    return generic_request(method="PUT", url=url, headers=headers, params=params, payload=payload, response_as_json=res_as_json)


def delete_request(url: str, headers: dict = None, params=None, payload=None, res_as_json: bool = None):
    url = url
    payload = payload
    headers = headers

    return generic_request(method="DELETE", url=url, headers=headers, params=params, payload=payload, response_as_json=res_as_json)


# endregion


# endregion
