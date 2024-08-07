
# -*- coding: utf-8 -*-
# 1 : imports of python lib
import hashlib
import hmac
from datetime import datetime
from requests import Request, Response
from timpypi.utils import exception


@exception
def request(method, domain, api, headers, body, params, ttype) -> Response:
    """ Custom request special for TikTok API
    :param Request method: one of `get`, `post`, `put`, `patch`, `delete`
    :param str domain: one of `https://auth.tiktok-shops.com` or ```https://open-api.tiktokglobalshop.com```
    :param str api: api special for request. example: `/authorization/202309/shops`
    :param dict headers: header for request.
    :param dict body:
    :param dict params: query
    :param str ttype: `data` or `json`
    :return: Response
    """
    if "timestamp" not in params.keys():
        params["timestamp"] = str(int(datetime.timestamp(datetime.now())))
    pairs = [f"{key}={value}" for key, value in params.items()]
    url = domain + api + "?" + "&".join(pairs)
    if ttype == "json":
        return method(url, params=params, headers=headers, json=body)
    return method(url, params=params, headers=headers, data=body)


@exception
def signature(api: str, params: dict, secret: str) -> str:
    """ Signature for each request to TikTok open API.
    :param str api: api special for request. example: `/authorization/202309/shops`
    :param dict params: query
    :param str secret:
    :return: str
    """
    keys = [key for key in params if key not in ["sign", "access_token"]]
    keys.sort()
    input = "".join(key + params[key] for key in keys)
    input = secret + api + input + secret
    signature = hmac.new(secret.encode(), input.encode(),
                         hashlib.sha256).hexdigest()
    return signature


@exception
def signatureWithBody(api: str, params: dict, body: bytes, secret: str) -> str:
    """ Signature with body for each request to TikTok open API.
    :param str api: api special for request. example: `/authorization/202309/shops`
    :param dict params: query
    :param str secret:
    :param bytes body:
    :return: str
    """
    keys = [key for key in params if key not in ["sign", "access_token"]]
    keys.sort()
    input = "".join(key + params[key] for key in keys)
    input = secret + api + input + body.decode("utf-8") + secret
    signature = hmac.new(secret.encode(), input.encode(),
                         hashlib.sha256).hexdigest()
    return signature
