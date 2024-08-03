from datetime import datetime
from typing import Literal

from pydantic import BaseModel


MongoFilters = dict[str, dict[str, dict[str, int | str | list[str]]]]

AdditionalFields = Literal["email", "phone", "website", "nace_codes", "social_medias"]

Country = Literal["BE", "FR", "NL"]
all_countries: list[Country] = ["BE", "FR", "NL"]

Region = Literal["bruxelles", "flamande", "wallonne"]
all_regions: list[Region] = ["bruxelles", "flamande", "wallonne"]

LegalFormType = Literal[None, "for-profit", "non-profit", "public"]
all_legal_form_types: list[LegalFormType] = [None, "for-profit", "non-profit", "public"]

EmployeeCategory = Literal[
    "0 employees",
    "1 to 4 employees",
    "5 to 9 employees",
    "10 to 19 employees",
    "20 to 49 employees",
    "50 to 99 employees",
    "100 to 199 employees",
    "200 to 499 employees",
    "500 to 999 employees",
    "1000 to 9999999 employees",
]
all_employee_categories: list[EmployeeCategory] = [
    "0 employees",
    "1 to 4 employees",
    "5 to 9 employees",
    "10 to 19 employees",
    "20 to 49 employees",
    "50 to 99 employees",
    "100 to 199 employees",
    "200 to 499 employees",
    "500 to 999 employees",
    "1000 to 9999999 employees",
]

LegalForm = Literal[
    "Agricultural company",
    "Autonomous municipal company",
    "Autonomous provincial company",
    "Brussels-Capital region authority",
    "CPAS / OCMW Association",
    "Cities and municipalities",
    "Co-ownership association",
    "Common law company",
    "Company or association without legal personality",
    "Congolese company",
    "Cooperative society",
    "Cooperative society (old regime)",
    "Cooperative society governed by public law",
    "Cooperative society governed by public law (old regime)",
    "Cooperative society with limited liability",
    "Cooperative society with limited liability (profit share)",
    "Cooperative society with limited liability and a social objective",
    "Cooperative society with limited liability governed by public law",
    "Cooperative society with unlimited liability",
    "Cooperative society with unlimited liability (profit share)",
    "Cooperative society with unlimited liability and a social objective",
    "Economic interest grouping with a social objective",
    "Economic interest grouping with registered seat in Belgium",
    "Europ. Econ. assoc wo reg.seat but with est. unit in Belgium",
    "European company (Societas Europaea)",
    "European cooperative society",
    "European economic assoc with registered seat in Belgium",
    "European political foundation",
    "European political party",
    "Federal public planning service",
    "Federal public service",
    "Flemish region and Flemish community authority",
    "Foreign ent. with property in Belgium (without legal pers.)",
    "Foreign entity",
    "Foreign entity with property in Belgium (with legal personality)",
    "Foreign entity without Belgian establishment unit with VAT representation",
    "Foreign listed company without Belgian establishment unit",
    "Foreign or international public organisations",
    "French community authority",
    "General partnership",
    "General partnership with a social objective",
    "German-speaking community authority",
    "Health fund / Mutual health insurance / National union of health funds",
    "Hulpverleningszone",
    "Intercommunal",
    "International non-profit association",
    "International non-profit association governed by public law",
    "International scientific organisation under Belgian law",
    "Limited partnership",
    "Limited partnership governed by public Law",
    "Local police",
    "Ministry for Middle Class",
    "Ministry of Economic Affairs",
    "Ministry of Foreign Affairs",
    "Ministry of Home Affairs",
    "Ministry of Justice",
    "Ministry of the Brussels-Capital Region",
    "Ministry of the Flemish Community",
    "Ministry of the French Community",
    "Ministry of the Walloon Region",
    "Miscellaneous",
    "Miscellaneous without legal personality",
    "Non-profit institution",
    "Non-profit organisation",
    "Ordinary limited partnership",
    "Ordinary limited partnership with a social objective",
    "Organis. regist. with the public admin. Pensions (Finance)",
    "Organisations registered with the O.N.P",
    "Other federal services",
    "Other institution with a social objective (public)",
    "Other legal form",
    "Other private organisation with legal personality",
    "Partnership limited by shares",
    "Partnership limited by shares with a social objective",
    "Pawnshop",
    "Pension scheme organisation",
    "Polders and water boards",
    "Private foreign association with establishment in Belgium",
    "Private foundation",
    "Private limited company",
    "Private limited company governed by public law",
    "Private limited liability company",
    "Private limited liability company with a social objective",
    "Private mutual insurance fund",
    "Professional corporations - Orders",
    "Professional union",
    "Project association",
    "Provincial authority",
    "Pubic social action centre",
    "Public institution",
    "Public limited company",
    "Public limited company with a social objective",
    "Public non-profit association",
    "Public utility foundation",
    "Public utility institution",
    "Representative association (Flemish region)",
    "Service provider association (Flemish region)",
    "State, Province, Region, Community",
    "Temporary association",
    "The services of the Prime Minister",
    "Trade union",
    "Unkown legal form (NSSO)",
    "VAT-group",
    "Walloon region authorit",
]
all_legal_forms: list[LegalForm] = [
    "Agricultural company",
    "Autonomous municipal company",
    "Autonomous provincial company",
    "Brussels-Capital region authority",
    "CPAS / OCMW Association",
    "Cities and municipalities",
    "Co-ownership association",
    "Common law company",
    "Company or association without legal personality",
    "Congolese company",
    "Cooperative society",
    "Cooperative society (old regime)",
    "Cooperative society governed by public law",
    "Cooperative society governed by public law (old regime)",
    "Cooperative society with limited liability",
    "Cooperative society with limited liability (profit share)",
    "Cooperative society with limited liability and a social objective",
    "Cooperative society with limited liability governed by public law",
    "Cooperative society with unlimited liability",
    "Cooperative society with unlimited liability (profit share)",
    "Cooperative society with unlimited liability and a social objective",
    "Economic interest grouping with a social objective",
    "Economic interest grouping with registered seat in Belgium",
    "Europ. Econ. assoc wo reg.seat but with est. unit in Belgium",
    "European company (Societas Europaea)",
    "European cooperative society",
    "European economic assoc with registered seat in Belgium",
    "European political foundation",
    "European political party",
    "Federal public planning service",
    "Federal public service",
    "Flemish region and Flemish community authority",
    "Foreign ent. with property in Belgium (without legal pers.)",
    "Foreign entity",
    "Foreign entity with property in Belgium (with legal personality)",
    "Foreign entity without Belgian establishment unit with VAT representation",
    "Foreign listed company without Belgian establishment unit",
    "Foreign or international public organisations",
    "French community authority",
    "General partnership",
    "General partnership with a social objective",
    "German-speaking community authority",
    "Health fund / Mutual health insurance / National union of health funds",
    "Hulpverleningszone",
    "Intercommunal",
    "International non-profit association",
    "International non-profit association governed by public law",
    "International scientific organisation under Belgian law",
    "Limited partnership",
    "Limited partnership governed by public Law",
    "Local police",
    "Ministry for Middle Class",
    "Ministry of Economic Affairs",
    "Ministry of Foreign Affairs",
    "Ministry of Home Affairs",
    "Ministry of Justice",
    "Ministry of the Brussels-Capital Region",
    "Ministry of the Flemish Community",
    "Ministry of the French Community",
    "Ministry of the Walloon Region",
    "Miscellaneous",
    "Miscellaneous without legal personality",
    "Non-profit institution",
    "Non-profit organisation",
    "Ordinary limited partnership",
    "Ordinary limited partnership with a social objective",
    "Organis. regist. with the public admin. Pensions (Finance)",
    "Organisations registered with the O.N.P",
    "Other federal services",
    "Other institution with a social objective (public)",
    "Other legal form",
    "Other private organisation with legal personality",
    "Partnership limited by shares",
    "Partnership limited by shares with a social objective",
    "Pawnshop",
    "Pension scheme organisation",
    "Polders and water boards",
    "Private foreign association with establishment in Belgium",
    "Private foundation",
    "Private limited company",
    "Private limited company governed by public law",
    "Private limited liability company",
    "Private limited liability company with a social objective",
    "Private mutual insurance fund",
    "Professional corporations - Orders",
    "Professional union",
    "Project association",
    "Provincial authority",
    "Pubic social action centre",
    "Public institution",
    "Public limited company",
    "Public limited company with a social objective",
    "Public non-profit association",
    "Public utility foundation",
    "Public utility institution",
    "Representative association (Flemish region)",
    "Service provider association (Flemish region)",
    "State, Province, Region, Community",
    "Temporary association",
    "The services of the Prime Minister",
    "Trade union",
    "Unkown legal form (NSSO)",
    "VAT-group",
    "Walloon region authorit",
]


class LeadGenerationCompanyFilters(BaseModel):
    additional_fields: list[AdditionalFields] | None = ["email", "phone", "website", "nace_codes", "social_medias"]

    countries: list[Country] = all_countries
    regions: list[Region] = all_regions
    zipcodes: list[str] | None = None
    declared_best_nace_codes: list[str] | None = None
    inoopa_best_nace_codes: list[str] | None = None

    minimum_number_of_estanlishments: int = 0
    maximum_number_of_estanlishments: int = 100000000000
    employee_categories: list[EmployeeCategory] = all_employee_categories
    created_before: datetime | None = datetime(year=2100, month=1, day=1)
    created_after: datetime | None = datetime(year=1500, month=1, day=1)
    include_decision_makers: bool = False

    max_results: int | None = None
    excluded_companies: list[str] | None = None

    legal_form_types: list[LegalFormType] = all_legal_form_types
    legal_forms: list[LegalForm] = all_legal_forms


class EnrichmentCompanyFilters(BaseModel):
    vats_to_enrich: list[str]
    country: Country = "BE"
    additional_fields: list[AdditionalFields] = ["email", "phone", "website", "nace_codes", "social_medias"]
    include_decision_makers: bool = False
