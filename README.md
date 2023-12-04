# Israel mock data generator

Tools that help to generate realistic mock data for Israel oriented use-cases.

## Faker Provider

The main functionality is based on a [faker](https://faker.readthedocs.io/) provider.

### Example Usage

```
from faker import Faker
from faker_israel import Provider as IsraelProvider
fake = Faker('he_IL')
fake.add_provider(IsraelProvider)
print(fake_en.bank_name())
print(fake_en.address())
```

### Reference

#### Supported locales

* `he_IL` - Hebrew
* `en_US` - English but Israel oriented data, e.g. street names will be in English but will resemble Israeli street names.

#### Providers / Methods

* `teudat_zehut()` - returns a valid Israeli ID number
* `het_pey()` - returns a valid Israeli company number (ח.פ.)
* Standard [address](https://faker.readthedocs.io/en/master/providers/faker.providers.address.html) provider but with Israeli street and city names
* Standard [company](https://faker.readthedocs.io/en/master/providers/faker.providers.company.html) provider but with Israeli company names
* Banks - 
  * `bank()` - return a bank dict with all it's details, can be passed to other bank methods to get details for the same bank
  * `bank_name()` - short bank name
  * `bank_full_name()` - full bank name
  * `bank_branch_name(bank)` - branch name
