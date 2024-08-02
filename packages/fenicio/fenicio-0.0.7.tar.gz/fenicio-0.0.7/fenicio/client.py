from requests import Response

from fenicio.orders import ParamsOrdersGET
from fenicio.request import get_orders, get_order

class Fenicio:
    """
    ### Fenicio Python SDK
    - https://developers.fenicio.help/es/apiv1/intro
    """
    def __init__(self, url_base: str):
        self.url_base = url_base.strip("/")
    
    def get_orders(self, *, params: ParamsOrdersGET = None) -> Response:
        return get_orders(url_base=self.url_base, params=params)

    def get_order(self, *, idOrden: str | int) -> Response:
        return get_order(url_base=self.url_base, idOrden=idOrden)
