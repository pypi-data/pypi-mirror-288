# from dataclasses import dataclass, field
from typing import Literal, Optional

from pydantic import AliasChoices, BaseModel, Field, StringConstraints
from typing_extensions import Annotated

from . import dkim, dmarc, spf

# https://en.wikipedia.org/wiki/List_of_DNS_record_types
TYPES_VALUES = Literal[
    "A",
    "AAAA",
    "CNAME",
    "MX",
    "NS",
    "PTR",
    "TXT",
]

FULL_COMPARISON = {
    "A",
    "AAAA",
    "CNAME",
}

UNIQUE_BY_NAME = {"MX", "NS", "PTR", "TXT"}


text = Annotated[str, StringConstraints(strip_whitespace=True)]


def is_apex(name: str) -> bool:
    return name.strip() in ("", "@")


def is_apex_dkim(name: str) -> bool:
    parts = name.split("_domainkey", 1)
    if len(parts) < 2:
        return False
    subdomain = parts[1].strip().rstrip(".")
    return is_apex(subdomain)


def is_apex_dmarc(name: str) -> bool:
    parts = name.split("_dmarc", 1)
    if len(parts) < 2:
        return False
    subdomain = parts[1].strip().rstrip(".")
    return is_apex(subdomain)


class Record(BaseModel):
    name: text
    type: str
    value: text = Field(validation_alias=AliasChoices("value", "data"))
    ttl: int = 3600
    id: Optional[text] = None
    zone: Optional[text] = None

    class Config:
        # populate_by_name = True
        extra = "ignore"

    def __eq__(self, __value: object) -> bool:
        """
        This method check the identity (e.g. same id if defined, or same name/name+value)
        """
        if not isinstance(__value, Record):
            return NotImplemented
        return self.are_equals(__value)
        # return self.identifier == __value.identifier

    def are_equals(self, __value: "Record") -> bool:
        """
        This method check the identity (e.g. same id if defined, or same name/name+value)
        """
        if self.id and __value.id:
            return self.id == __value.id
        if (self.normalized_name, self.type) != (__value.normalized_name, __value.type):
            return False
        if self.type in FULL_COMPARISON:
            return self.value == __value.value
        return True

    @property
    def normalized_name(self):
        """ """
        return self.name or "@"

    @property
    def identifier(self) -> str:
        """
        This method returns an identifer for the record that does not depend on its remote id
        """
        identifier = f"{self.normalized_name}/{self.type}"
        if self.type in FULL_COMPARISON:
            identifier = f"{identifier}/{self.value}"
        return identifier

    def __hash__(self):
        return hash(self.identifier)

    @property
    def contains_spf_definition(self) -> bool:
        """
        Return true if the record's content is a SPF definition.
        The record does not be for the APEX.
        e.g. spf1.mydomain.com can return True
        """
        # RFC states that we only have one spf record on the APEX
        # But we may defined other records with spf definition to be included elsewhere.
        return all((self.type == "TXT", spf.is_spf(self.value)))

    @property
    def is_apex(self) -> bool:
        return is_apex(self.name)

    @property
    def is_spf(self) -> bool:
        """
        Return true if the record is a valid SPF record.
        The record MUST be for the APEX
        e.g. spf1.mydomain.com will always return False
        """
        # RFC:
        # https://www.rfc-editor.org/rfc/rfc6242#section-4.1
        # https://datatracker.ietf.org/doc/html/rfc7208#section-4.5
        # NOTE: There should be only 1 apex spf record,
        # but we can create other spf record (e.g. spf1.mydomain.com) and include it in the apex
        # (alternatively, we can define spf records with CNAME or even NS records)
        return all((self.is_apex, self.contains_spf_definition))

    def spf(self) -> spf.SPF:
        if not self.is_spf:
            raise Exception("Record is not an SPF record")
        return spf.parse_spf(self.value)

    @property
    def is_dkim(self) -> bool:
        """
        This function TRIES to guess if the record is a DKIM one.
        There is no required and obvious way to define a dkim record.

        As a last resort, we will try to parse the record.
        """
        # https://www.rfc-editor.org/rfc/rfc6376#section-3.6.1
        if self.type != "TXT":
            return False
        # DKIM record might not contain _domainkey
        # if it is referenced with a CNAME/PTR/... record
        if "._domainkey" in self.name:
            return True
        if self.value.lstrip().startswith("v=DKIM1"):
            return True
        # Try to parse it as a last resort
        try:
            self.parse_dkim(coalesce=False, ensure_b64_encoding=False)
            return True
        except Exception:
            return False

    def parse_dkim(self, coalesce=True, ensure_b64_encoding=True) -> dict:
        """
        Parse the dkim record and return a key-value dict.
        It will raise an exception if the record is not a valid DKIM record.

        coalesce: Add default values if not explicitly defined in the record
        """
        if self.type != "TXT":
            raise Exception("Record is not of type TXT")
        return dkim.parse_dkim(
            self.value, coalesce=coalesce, ensure_b64_encoding=ensure_b64_encoding
        )

    @property
    def dkim(self) -> dkim.DKIM:
        return dkim.DKIM.from_string(self.value)

    @property
    def is_dmarc(self) -> bool:
        if not all(("_dmarc" in self.name, self.type == "TXT")):
            return False
        return dmarc.is_dmarc(self.value)

    @property
    def is_null_mx(self) -> bool:
        return (
            self.type.upper() == "MX"
            and (self.name.endswith(".") or self.name in ("", "@"))
            and self.value in ("", ".")
        )

    def is_standard_default(self):
        return any((self.is_spf, self.is_dkim, self.is_dmarc, self.is_null_mx))


__all__ = [
    "Record",
]
