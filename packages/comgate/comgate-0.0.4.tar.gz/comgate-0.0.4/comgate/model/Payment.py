import dataclasses
from typing import List, Optional
from comgate.enum.PaymentMethodCodeEnum import PaymentMethodCodeEnum
from comgate.enum.CountryCodeEnum import CountryCodeEnum
from comgate.enum.CurrencyCodeEnum import CurrencyCodeEnum
from comgate.enum.LanguageCodeEnum import LanguageCodeEnum


@dataclasses.dataclass
class Payment:
    price: int
    curr: CurrencyCodeEnum
    label: str
    ref_id: str
    email: str
    phone: str
    full_name: str
    prepare_only: bool
    lang: LanguageCodeEnum = LanguageCodeEnum.CS
    country: CountryCodeEnum = CountryCodeEnum.ALL
    payer_id: Optional[str] = None
    account: Optional[str] = None
    name: Optional[str] = None
    pre_auth: Optional[bool] = None
    init_recurring: Optional[bool] = None
    verification: Optional[bool] = None
    embedded: Optional[bool] = None
    eet_report: Optional[bool] = None
    eet_data: Optional[dict] = None
    included_methods: Optional[List[PaymentMethodCodeEnum]] = None
    excluded_methods: Optional[List[PaymentMethodCodeEnum]] = None

    def to_dict(self) -> dict:
        method = '+'.join([i.value for i in self.included_methods]) if self.included_methods else ''
        if self.excluded_methods:
            method += '-' + '-'.join([e.value for e in self.excluded_methods])

        return {
            'price': self.price,
            'curr': self.curr.value,
            'label': self.label,
            'refId': str(self.ref_id),
            'method': method,
            'country': self.country.value,
            'lang': self.lang.value,
            'email': self.email,
            'phone': self.phone,
            'fullName': self.full_name,
            'prepareOnly': 'true' if self.prepare_only else 'false',
        }
