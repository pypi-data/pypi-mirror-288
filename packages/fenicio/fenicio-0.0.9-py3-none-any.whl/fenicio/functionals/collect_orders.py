from typing import List
from fenicio.client import Fenicio
from fenicio.orders import ParamsOrdersGET, FenicioOrders

def download_all_orders_responses(fenicio: Fenicio, params: ParamsOrdersGET) -> List[dict]:
    responses = []
    flag = True
    i = 1
    while flag:
        params.pag = i
        r = fenicio.get_orders(params=params).json()   # TODO: Atajar caso `error=True`
        if len(r["ordenes"]) == 0:
            flag = False
        else:
            responses.append(r)
            total_orders = sum(len(r["ordenes"]) for r in responses)
            print(f"total_orders: {total_orders} | page: {i} | totAbs: {responses[-1]['totAbs']}")
            i += 1
    return responses

def download_all_orders(fenicio: Fenicio, params: ParamsOrdersGET) -> FenicioOrders:
    # FIXME: Hardcodeado, y no se controla un error=True, o si la requests falla.
    responses = download_all_orders_responses(fenicio=fenicio, params=params)
    totAbs = 0 if len(responses)==0 else responses[-1]["totAbs"]
    orders = FenicioOrders(
        error = False,
        msj = "",
        totAbs = totAbs,
        ordenes = []
    )
    for r in responses:
        orders.ordenes.extend(FenicioOrders(**r).ordenes)
    return orders
