from pydantic import BaseModel, ConfigDict

class BaseModelNoExtra(BaseModel):
    model_config = ConfigDict(extra="forbid")   # Tira error si se agregan campos que no existen.