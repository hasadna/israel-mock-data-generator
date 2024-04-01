from functools import partial

from .north import SalaryNorth
from .south import SalarySouth

SALARIES = {k: partial(v, k) for k, v in {
    'north': SalaryNorth,
    'south': SalarySouth,
}.items()}
