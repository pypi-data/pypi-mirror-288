from .suffixes import (
    find_suffix,
    get_organizational_name,
    get_public_suffixes,
    is_organizational_name,
)
from .whois import Whois


def normalize_domainname(name: str) -> str:
    return ".".join(p.strip() for p in name.lower().split("."))


def is_arpa(domainname):
    return domainname.lower().rstrip(".").endswith(".arpa")
