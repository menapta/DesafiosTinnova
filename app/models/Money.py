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

