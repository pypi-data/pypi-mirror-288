from typing import Literal
import os

import requests
from requests import Response

CobroswapCurrency = Literal["UYU"]

def url_create_payment_link() -> str:
    """ FIXME: Esto es genérico?"""
    return "https://cobroswap.com/api/banking/createExternalPayment"

def _get_json_create_payment_link(*, amount: float, currency: CobroswapCurrency) -> dict:
    """ TODO: Ver `concept` y `companyId`."""
    return {
        "amount": amount,
        "currency": currency,                                   # FIXME: Que monedas acepta?
        "concept": "Membresia 3 meses",                         # FIXME: Hardcodeado.
        "companyId": os.getenv("COMPANY_ID")                    # FIXME: Dato sensible?
    }

def response_create_payment_link(*, amount: float, currency: CobroswapCurrency) -> Response:
    url = url_create_payment_link()
    json_ = _get_json_create_payment_link(amount=amount, currency=currency)
    return requests.post(url=url, json=json_)

def create_payment_link(*, amount: float, currency: CobroswapCurrency) -> str | None:
    r = response_create_payment_link(amount=amount, currency=currency)
    if not(200 <= r.status_code <= 299):
        return None
    url_payment = r.json()["paymentLink"]["url"]
    return url_payment
