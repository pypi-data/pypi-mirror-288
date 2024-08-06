import os
import pytest
from requests import Response

from fenicio.request import get_order, get_orders
from fenicio.orders import FenicioOrders, ParamsOrdersGET, FenicioOrder

@pytest.fixture
def url_base() -> str:
    url = os.getenv("TEST_FENICIO_URL")
    if url is None:
        raise ValueError("Se debe configurar una url de testing.")
    return url

@pytest.fixture
def idOrder_example(url_base) -> str:
    """ Se hace una query para obtener un idOrden"""
    params = ParamsOrdersGET(tot=1)
    r = get_orders(url_base=url_base, params=params)
    idOrden = FenicioOrders(**r.json()).ordenes[0].idOrden
    return idOrden


def _assert_r_get_order_orders(r: Response) -> dict:
    """ Agrupo las 2 requests, por que ambas tienen el campo 'error' y se espera 200."""
    r_json = r.json()
    assert r_json["error"] == False
    assert r.status_code == 200
    return r_json

def test_get_orders_no_params(url_base) -> None:
    r = get_orders(url_base=url_base)
    r_json = _assert_r_get_order_orders(r=r)
    orders = FenicioOrders(**r_json)

def test_get_orders_state_abandonada(url_base) -> None:
    params = ParamsOrdersGET(tot=1, estado="ABANDONADA")
    r = get_orders(url_base=url_base, params=params)
    r_json = _assert_r_get_order_orders(r=r)
    orders = FenicioOrders(**r_json)

def test_order(url_base, idOrder_example) -> None:
    r = get_order(url_base=url_base, idOrden=idOrder_example)
    r_json = _assert_r_get_order_orders(r=r)
    order = FenicioOrder(**r_json["orden"])
