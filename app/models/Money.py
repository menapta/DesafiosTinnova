from decimal import Decimal
from typing import Annotated

from pydantic import AfterValidator
def validateDecimal(v: Decimal) -> Decimal:
    if v.as_tuple().exponent < -2:
        raise ValueError("O preço deve ter no máximo duas casas decimais (ex: 10.55)")
    return v

Money = Annotated[Decimal, AfterValidator(validateDecimal)]