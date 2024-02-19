from functools import partial

from .north import BankNorth
from .south import BankSouth
from .moon import BankMoon
from .sun import BankSun
from .earth import BankEarth

BANKS = {k: partial(v, k) for k, v in {
    'north': BankNorth,
    'south': BankSouth,
    'earth': BankEarth,
    'moon': BankMoon,
    'sun': BankSun,
}.items()}
