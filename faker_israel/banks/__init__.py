from functools import partial

from .poalim import BankPoalim
from .leumi import BankLeumi
from .discount import BankDiscount
from .mizrahi import BankMizrahi
from .fibi import BankFibi
from .yahav import BankYahav


BANKS = {k: partial(v, k) for k, v in {
    'poalim': BankPoalim,
    'leumi': BankLeumi,
    'discount': BankDiscount,
    'mizrahi': BankMizrahi,
    'fibi': BankFibi,
    'yahav': BankYahav,
}.items()}
