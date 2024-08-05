"""
Utilities to get and parse WHOIS database

WARNING: There are legal involvement here (especially part 2):
    By submitting a WHOIS query, you agree that you will use this data
    only for lawful purposes and that, under no circumstances, you will
    use this data to
    1) allow, enable, or otherwise support the transmission of mass
    unsolicited, commercial advertising or solicitations via E-mail
    (spam) or
    2) enable high volume, automated, electronic processes that apply
    to this WHOIS server.
    These terms may be changed without prior notice.
    By submitting this query, you agree to abide by this policy.

Therefore, these requests should not be abused.
Ideally, and if possible, prefer to retrieve the informations
from the registrar's API directly
"""

import logging
from typing import Any, Dict, List, Optional

import whois
from pydantic import BaseModel, StringConstraints, ValidationError
from typing_extensions import Annotated

text = Annotated[str, StringConstraints(strip_whitespace=True)]


def try_fallback(data, keys, default=None):
    _sentinel = object()
    for k in keys:
        res = data.get(k, _sentinel)
        if res is not _sentinel:
            return res
    return default


class Whois(BaseModel):
    name: text
    registrar: Optional[text]
    registrar_url: Optional[text]
    nameservers: List[text]
    data: Dict[str, Any]

    class Config:
        populate_by_name = True
        extra = "ignore"

    @classmethod
    def whois(cls, domain: str, no_raise=True) -> Optional["Whois"]:
        try:
            res = whois.whois(domain)
            domain_name = res.get("domain_name")
            # if isinstance(domain_name, (list, tuple)):
            if not isinstance(domain_name, str):
                if all(v is None for v in res.values()):
                    raise Exception("No data retrieved")
                domain_name = domain
            nameservers = res.get("name_servers") or []
            # Formatting is not standard
            if isinstance(nameservers, str):
                nameservers = nameservers.split("\n\n")[0]
                nameservers = [ns.strip() for ns in nameservers.split("\n")]
            nameservers = list({ns.lower() for ns in nameservers if ns})
            registrar = try_fallback(res, ("registrar",))
            registrar_url = try_fallback(res, ("registrar_url",))
            return Whois(
                name=domain_name,
                registrar=registrar,
                registrar_url=registrar_url,
                nameservers=nameservers,
                data=res,
            )
        except Exception as e:
            if no_raise:
                if isinstance(e, ValidationError):
                    logging.error(e)
                else:
                    logging.debug(e)
                return None
            raise
