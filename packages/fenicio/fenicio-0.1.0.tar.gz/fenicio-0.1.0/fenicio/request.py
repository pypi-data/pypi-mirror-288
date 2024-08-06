import requests
from requests import Response

from fenicio.url import url_get_orders, url_get_order
from fenicio.orders import ParamsOrdersGET

def get_orders(*, url_base: str, params: ParamsOrdersGET = None) -> Response:
    """ https://developers.fenicio.help/es/apiv1/ordenes-listar"""
    if params is None:
        params = ParamsOrdersGET()
    url = url_get_orders(url_base=url_base)
    return requests.get(url=url, params=params.to_json())

def get_order(*, url_base: str, idOrden: str | int) -> Response:
    """ https://developers.fenicio.help/es/apiv1/orden-recuperar"""
    url = url_get_order(url_base=url_base, idOrden=idOrden)
    return requests.get(url=url)
