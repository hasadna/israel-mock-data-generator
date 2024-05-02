from functools import partial

from .north import SalaryNorth
from .south import SalarySouth
from .east import SalaryEast
from .west import SalaryWest

SALARIES = {k: partial(v, k) for k, v in {
    'north': SalaryNorth,
    'south': SalarySouth,
    'east': SalaryEast,
    'west': SalaryWest,
}.items()}
