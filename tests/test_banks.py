import dataflows as DF
from faker import Faker

from faker_israel.banks import BANKS
from faker_israel import Provider as IsraelProvider


def test():
    fake = Faker('he_IL')
    israel_provider = IsraelProvider(fake)
    fake.add_provider(israel_provider)

    def iterator():
        for bank_class in BANKS.values():
            bank = bank_class(israel_provider)
            for branch in bank.iterate_all_branches():
                yield branch.as_dict()

    DF.Flow(
        iterator(),
        DF.dump_to_path('.data/bank_branches'),
        DF.printer()
    ).process()
