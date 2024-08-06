VERSION = "API_V1"

def url_get_orders(*, url_base: str) -> str:
    return f"{url_base}/{VERSION}/ordenes"

def url_get_order(*, url_base: str, idOrden: str) -> str:
    return f"{url_base}/{VERSION}/ordenes/{idOrden}"