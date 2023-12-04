from faker.providers import ElementsType

from faker.providers.company import Provider as BaseCompanyProvider


class CompanyHeProvider(BaseCompanyProvider):
    formats: ElementsType[str] = (
        "{{last_name}} {{company_suffix}}",
        "{{last_name}}-{{last_name}}",
        "{{last_name}}, {{last_name}} ו{{last_name}}",
    )
    company_suffixes: ElementsType[str] = ('בע"מ', "ובניו", 'ע"ר')
