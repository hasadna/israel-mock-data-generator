from functools import partial

from .north import SalaryNorth

SALARIES = {k: partial(v, k) for k, v in {
    'north': SalaryNorth,
}.items()}
