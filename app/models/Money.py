from decimal import Decimal, ROUND_HALF_UP
from typing import Annotated
from pydantic import AfterValidator, PlainSerializer

def validate_money(v: Decimal) -> Decimal:
    return v.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

Money = Annotated[
    Decimal, 
    AfterValidator(validate_money),
    PlainSerializer(lambda v: "{:.2f}".format(v), return_type=str)
]

# from decimal import Decimal, ROUND_HALF_UP
# from typing import Annotated
# from pydantic import AfterValidator

# def validateDecimal(v: Decimal) -> Decimal:
#     if v.as_tuple().exponent < -2:
#         raise ValueError("O preço deve ter no máximo duas casas decimais (ex: 10.55)")

#     return v.quantize(Decimal("0.00"), rounding=ROUND_HALF_UP)

# Money = Annotated[Decimal, AfterValidator(validateDecimal)]

# from decimal import Decimal
# from typing import Annotated

# from pydantic import AfterValidator
# def validateDecimal(v: Decimal) -> Decimal:
#     if v.as_tuple().exponent < -2:
#         raise ValueError("O preço deve ter no máximo duas casas decimais (ex: 10.55)")
#     return v

# Money = Annotated[Decimal, AfterValidator(validateDecimal)]