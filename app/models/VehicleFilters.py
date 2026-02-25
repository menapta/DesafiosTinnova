from typing import Optional
from pydantic import  BaseModel, model_validator

from .Money import Money


class VehicleFilters(BaseModel):
    ano: Optional[int] = None 
    marca: Optional[str] = None
    cor: Optional[str] = None
    minPreco: Optional[Money] = None
    maxPreco: Optional[Money] = None

    @model_validator(mode='after')
    def validateFilters(self):
        if self.minPreco is not None and self.maxPreco is not None:
            if self.minPreco > self.maxPreco:
                raise ValueError("minPreco não pode ser maior que maxPreco")

        featureFields = [self.ano, self.marca, self.cor]
        if any(featureFields) and not all(featureFields):
             raise ValueError("Se um dos campos (ano, marca, cor) for preenchido, todos os outros dois também devem ser.")

        if (self.minPreco is not None) != (self.maxPreco is not None):
            raise ValueError("Para filtrar por preço, você deve enviar tanto minPreco quanto maxPreco")
            
        return self