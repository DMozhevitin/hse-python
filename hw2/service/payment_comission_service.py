from exception.exceptions import IllegalArgumentException

RATE = 0.05

def calculate_comission(amount: float) -> float:
    if amount <= 0:
        raise IllegalArgumentException('Expected positive amount, but got {}'.format(amount))
    return amount * RATE
