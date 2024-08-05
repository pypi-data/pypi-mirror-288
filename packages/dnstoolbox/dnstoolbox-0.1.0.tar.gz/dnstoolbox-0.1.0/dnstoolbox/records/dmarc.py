# from dataclasses import dataclass, field
import logging
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, PositiveInt, conint

from .utils import parse_tag_value

# https://www.rfc-editor.org/rfc/rfc6376#section-3.6.1
DMARC_TAGS = {
    "v",  #
    "adkim",  # DKIM Identifier Alignment mode (strict or relaxed)
    "aspf",  # SPF Identifier Alignment mode (strict or relaxed)
    "fo",  # Failure Reporting Options
    "p",  # Requested Mail Receiver Policy
    "sp",  # Mail Receiver policy for all subdomains
    "pct",  # Percentage of messages impacted
    "rf",  # Report Format
    "ri",  # Report Interval
    "rua",  # Aggregated Feedback Address
    "ruf",  # Message-Specific Report Address
}


class DMARC(BaseModel):
    v: Literal["DMARC1"] = "DMARC1"
    adkim: Literal["r", "s"] = "r"
    aspf: Literal["r", "s"] = "r"
    fo: Optional[str] = None
    p: Optional[str] = None
    # https://github.com/pydantic/pydantic/issues/5006
    pct: Optional[Annotated[int, conint(ge=0, le=100)]] = 100
    rf: Optional[str] = "afrf"
    ri: Optional[PositiveInt] = 86400
    rua: Optional[str] = None
    ruf: Optional[str] = None
    sp: Optional[str] = None

    @classmethod
    def from_string(cls, value, logger=None):
        try:
            res = parse_dmarc(value)
            return DMARC.model_validate(res)
        except Exception as e:
            (logger or logging).debug(e)
            return None


def is_dmarc(value, strict=True) -> bool:
    try:
        it = parse_tag_value(value)
        tag, version = next(it, ("", ""))
        if tag != "v":
            return False
        if not strict:
            version = version.upper()
        return version == "DMARC1"
    except Exception:
        return False


# https://www.rfc-editor.org/rfc/rfc7489#section-6.3
# https://www.rfc-editor.org/rfc/rfc7489#section-6.4
def parse_dmarc(value) -> dict:
    """
    Parse the dmarc record and return a key-value dict.
    It will raise an exception if the record is not a valid DMARC record.

    coalesce: Add default values if not explicitly defined in the record
    """
    # https://www.rfc-editor.org/rfc/rfc6376#section-3.2
    # https://www.rfc-editor.org/rfc/rfc6376#section-3.6.1
    tag_list = tuple(parse_tag_value(value))
    tags = {t for t, _ in tag_list}
    if "p" not in tags:
        raise Exception("Required tag 'p' is missing")
    extra_tags = tags - DMARC_TAGS
    if extra_tags:
        extra_tags_text = ", ".join(f"'{t}'" for t in extra_tags)
        raise Exception(
            f"The following non-standard tags are defined: {extra_tags_text}"
        )
    result = {}
    for i, (t, v) in enumerate(tag_list):
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
            if v != "DMARC1":
                raise Exception(
                    f"Tag 'v' contains invalid value {v} (case-sensitive check)"
                )
        result[t] = v
    return result


__all__ = [
    "DMARC",
]
