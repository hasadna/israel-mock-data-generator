import os
import json

from .bank import Bank, BankBranch


class BankPoalim(Bank):
    name = 'הפועלים'

    def iterate_all_branches(self, **kwargs):
        with open(os.path.join(os.path.dirname(__file__), '..', 'data', 'poalim_branches.json')) as f:
            for branch in json.load(f):
                if branch['branchTypeCode'] == 'PRV':
                    phone_number = None
                    for addr in branch['contactAddress']:
                        if addr['contactChannelTypeCode'] == 1 and len(addr.get('contactAddressInfo', '')) > 7:
                            phone_number = addr['contactAddressInfo']
                            break
                    for addr in branch['geographicAddress']:
                        city = addr.get('cityName')
                        street = addr.get('streetName')
                        building = addr.get('buildingNumber')
                        zip_code = addr.get('zipCode')
                        if all([city, street, building, zip_code]):
                            address = f'{street} {building}, {city}, {zip_code}'
                            break
                    yield BankBranch(
                        self, branch['branchName'], branch['branchNumber'],
                        phone_number=phone_number,
                        address=address,
                        manager_name=branch['branchManagerName'],
                        manager_phone_number=branch['branchManagerPhoneNumber'],
                        **kwargs
                    )
