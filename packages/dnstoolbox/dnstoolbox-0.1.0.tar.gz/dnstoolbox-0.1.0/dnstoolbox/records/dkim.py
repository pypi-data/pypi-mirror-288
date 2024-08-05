# from dataclasses import dataclass, field
import base64
import logging
from typing import Any, List, Optional

from pydantic import BaseModel

from .utils import parse_tag_value

# https://www.rfc-editor.org/rfc/rfc6376#section-3.6.1
DKIM_TAGS = {
    "v",  # Version of the DKIM key record (Optional, must be first if defined, default to DKIM1)
    "h",  # Acceptable hash algorithms (Optional, default to allowing all algorithms)
    "k",  # Key type (i.e. sign algorithm) (OPTIONAL, default is "rsa")
    "n",  # Notes that might be of interest to a human (no particular meaning) (OPTIONAL)
    "p",  # REQUIRED: public key encoded in base64
    "s",  # Service Type (Optional, default: "*"). colon-separated list of service types to which this record applies
    "t",  # Flags, only "y" and "s" flags are supported at the moment
}


class DKIM(BaseModel):
    p: str
    v: Optional[str] = "DKIM1"
    h: Optional[str] = None
    k: Optional[str] = "rsa"
    n: Optional[str] = None
    s: Optional[List[str]] = None
    t: Optional[List[str]] = None

    @classmethod
    def from_string(cls, value, logger=None):
        try:
            res = parse_dkim(value, coalesce=False, ensure_b64_encoding=True)
            return DKIM.model_validate(res)
        except Exception as e:
            (logger or logging).debug(e)
            return None


ALLOWED_DKIM_FLAGS = {"y", "s"}


def parse_dkim_flags(flags: Optional[str]) -> Optional[List[str]]:
    if flags is None:
        return None
    splitted_flags = {f.strip() for f in flags.split(",")}
    non_standard = splitted_flags - ALLOWED_DKIM_FLAGS
    if non_standard:
        non_standard_text = ",".join(non_standard)
        raise Exception(
            f"The following non-standard flags were found: {non_standard_text}"
        )
    return list(splitted_flags)


def parse_dkim_services(services: str) -> Optional[List[str]]:
    if services is None:
        return None
    return list({f.strip() for f in services.split(",")})


DKIM_TAGS_DEFAULT_VALUES = {
    "v": "DKIM1",
    "h": None,
    "k": "rsa",
    "n": None,
    # "p":  # REQUIRED => No default value
    "s": "*",
    "t": None,
}


def parse_dkim(value, coalesce=True, ensure_b64_encoding=True) -> dict:
    """
    Parse the dkim record and return a key-value dict.
    It will raise an exception if the record is not a valid DKIM record.

    coalesce: Add default values if not explicitly defined in the record
    """
    # https://www.rfc-editor.org/rfc/rfc6376#section-3.2
    # https://www.rfc-editor.org/rfc/rfc6376#section-3.6.1
    tag_list = tuple(parse_tag_value(value))
    tags = {t for t, _ in tag_list}
    if "p" not in tags:
        raise Exception("Required tag 'p' is missing")
    extra_tags = tags - DKIM_TAGS
    if extra_tags:
        extra_tags_text = ", ".join(f"'{t}'" for t in extra_tags)
        raise Exception(
            f"The following non-standard tags are defined: {extra_tags_text}"
        )
    result = {}
    for i, (t, tag_value) in enumerate(tag_list):
        v: Any = tag_value
        existing = result.get(t)
        if existing is not None:
            raise Exception(
                f"Tag '{v}' is redefined. Current value: '{v}', Previous value: {existing}"
            )
        if t == "v":
            if i != 0:
                raise Exception(
                    "version tag 'v' is defined but is not the first tag in the list"
                )
            if tag_value != "DKIM1":
                raise Exception(
                    f"Tag 'v' contains invalid value {v} (case-sensitive check)"
                )
        if t == "t":
            v = parse_dkim_flags(tag_value)
        if t == "s":
            v = parse_dkim_services(tag_value)
        result[t] = v
    if ensure_b64_encoding:
        pubkey = result["p"]
        try:
            base64.b64decode(pubkey)
        except Exception:
            raise Exception("Public Key 'p' is not correctly encoding in base64")
    if coalesce:
        result = {**DKIM_TAGS_DEFAULT_VALUES, **result}
    return result


__all__ = [
    "DKIM",
]
