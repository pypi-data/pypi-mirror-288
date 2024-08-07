"""This module contains the definition of the configurations and the respecting default values"""

from typing import List

from pydantic import BaseModel, PositiveInt


class PathConfig(BaseModel):
    """Config values for different resources"""

    invoices_dir: str = "/home/user/invoices/"
    html_template: str = "shiny_invoice/templates/default_en.html"
    datastore: str = "datastore.json"


class BankConfig(BaseModel):
    """Configuration of bank details"""

    name: str = "Some Bank"
    iban: str = "DE12 1234 5678 9100 00"
    bic: str = "BICCCCCCC"
    tax_number: str = "11/2222/3333"


class CompanyConfig(BaseModel):
    """Configuration of company details"""

    name: str = "Company Name"
    skills: List[str] = ["Primary Skill", "Secondary Skill"]
    address: List[str] = ["Address line 1", "4234 Addressline 2"]
    contact: List[str] = ["contact@shinyinvoice.de", "+49 123 456789", "shinyinvoice.de"]
    bank: BankConfig = BankConfig()
    tax_rate: float = 0.19
    payment_terms_days: PositiveInt = 14


class InvoiceDefaultsConfig(BaseModel):
    """Configuration of invoice defaults that should be rendered in the invoice"""

    introduction: str = "Dear Sir or Madam,"
    recipient: str = "Comp 2\nCompstreet Comp\n1335 Compvill"
    items: str = "Services, Hours, Rate, Price\nService 1, 40h, 100 €, 4.000 €"


class Config(BaseModel):
    """Shiny-Invoice configuration"""

    paths: PathConfig = PathConfig()
    company: CompanyConfig = CompanyConfig()
    invoice_defaults: InvoiceDefaultsConfig = InvoiceDefaultsConfig()
