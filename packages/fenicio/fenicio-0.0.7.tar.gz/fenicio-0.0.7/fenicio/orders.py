from typing import Literal, List
from datetime import datetime

from pydantic import BaseModel, Field

from fenicio._etc import BaseModelNoExtra


__all__ = ["FenicioOrders", "FenicioOrder", "ParamsOrdersGET"]

BuyerDocument = Literal["DOCUMENTO_IDENTIDAD", "PASAPORTE"]
Gender = Literal[None, "F", "M"]
OrderState = Literal[
    "EN_CURSO",
    "ABANDONADA",
    "PAGO_PENDIENTE",
    "REQUIERE_APROBACION",
    "APROBADA",
    "CANCELADA"
]
Country = Literal[
    "UY", "AR", "CL", "US", "AU", "ES", "CO",
    "PE", "BR", "BO", "PY", "CA", "RU", "MX",
    "NP", "UG", "UZ", "FR", "VE", "DE", "IT",
    "AT", "CN", "IL", "CR", "AS", "VN", "IN",
    "GB" # FIXME: No agregar manualmente, incluir todos los paises.
]
DeliveryState = Literal[
    None,
    "RECIBIDO",
    "PREPARANDO",
    "AGUARDANDO_DESPACHO",
    "EN_TRANSITO",
    "LISTO_PARA_RETIRAR",
    "ENTREGADO"
]



class ParamsOrdersGET(BaseModel):
    pag: int | None = Field(default=1, ge=1)
    tot: int = Field(default=50, ge=1, le=500)
    #fDesde: date = None
    estado: OrderState = None

    def to_json(self) -> dict:
        """ Retorna el JSON para usar en el requests."""
        return {k: v for k, v in self.model_dump().items() if v is not None}


class FenicioBuyerDocument(BaseModelNoExtra):
    numero: str
    pais: Country
    tipo: BuyerDocument

class FenicioBuyer(BaseModelNoExtra):
    id: int
    codigo: None
    email: str
    nombre: str | None
    apellido: str | None
    telefono: str | None
    genero: Gender
    documento: FenicioBuyerDocument | None
    extras: dict | None

class FenicioSchedule(BaseModelNoExtra):
    desde: datetime
    hasta: datetime

class FenicioDeliveryAddress(BaseModelNoExtra):
    latitud: float | None
    longitud: float | None
    pais: str
    estado: str
    localidad: str
    calle: str
    numeroPuerta: str
    numeroApto: str | None
    codigoPostal: str | None
    observaciones: str | None

class FenicioDeliveryService(BaseModelNoExtra):
    id: int
    codigo: str
    nombre: str

class FenicioDelivery(BaseModelNoExtra):
    tipo: Literal[None, "ENVIO", "RETIRO"]
    estado: DeliveryState
    horario: FenicioSchedule | None
    destinatario: str
    direccionEnvio: FenicioDeliveryAddress | None
    local: str | None
    servicioEntrega: FenicioDeliveryService | None
    codigoTracking: str | None
    etiqueta: str | None

class FenicioOrderProduct(BaseModelNoExtra):
    nombre: str
    sku: str
    cantidad: int
    cantidadRegalo: int
    codigoPrecio: str
    precio: float
    descuentos: list | None                 # TODO: Ver el modelo de datos.
    atributos: dict | None                  # TODO: Ver el modelo de datos.

class FenicioOrder(BaseModelNoExtra):
    """ https://developers.fenicio.help/es/referencias/modelos-de-datos?id=orden"""
    idOrden: str                            # String numérico.
    idOrdenOrigen: str
    numeroOrden: int                        # OBSOLETO: https://developers.fenicio.help/es/referencias/modelos-de-datos?id=orden
    referencia: str | None
    estado: OrderState
    motivoCancelacion: str | None
    origen: Literal["WEB", "CALLCENTER", "MERCADOLIBRE"]
    fechaInicio: datetime
    fechaAbandono: datetime | None
    fechaRecuperada: datetime | None
    fechaFin: datetime | None
    fechaCancelada: datetime | None
    comprador: FenicioBuyer | None
    direccionFacturacion: dict | None       # TODO: Ver su modelo de datos.
    codigoTributario: str | None
    razonSocial: str | None
    moneda: Literal["UYU"]
    pago: dict | None                       # TODO: Ver su modelo de datos.
    entrega: FenicioDelivery
    lineas: List[FenicioOrderProduct]
    impuestos: float
    importeTotal: int
    observaciones: str | None
    historialCallCenter: list

class FenicioOrders(BaseModelNoExtra):
    """ https://developers.fenicio.help/es/apiv1/ordenes-listar"""
    error: bool
    msj: str
    totAbs: int
    ordenes: List[FenicioOrder]
