# from dataclasses import dataclass, field
import logging
import re
from typing import List, Literal, Optional, Tuple, Union

import dns.resolver
from pydantic import BaseModel

# https://www.rfc-editor.org/rfc/rfc7208#section-4.6.1
MECANISMS = {"all", "include", "a", "mx", "ptr", "ip4", "ip6", "exists"}
# https://www.rfc-editor.org/rfc/rfc7208#section-4.6.4
MECANISMS_CAUSING_QUERIES = {"include", "a", "mx", "ptr", "exists"}
LOOKUP_LIMIT = 10

MODIFIERS = {
    "redirect",
    "explanation",
    # "unknown-modifier",
}

SPF_DIRECTIVE_REG = re.compile(
    r"(?P<qualifier>[+-\?~]?)(?P<mecanism>all|include|a|mx|ptr|ip4|ip6|exists)((?P<with_data>:|/)(?P<data>.*))?",
    re.IGNORECASE,
)

SPF_VERSION = "v=spf1"


DirectiveQualifier = Literal[
    "+",
    "-",
    "?",
    "~",
]
DirectiveMecanism = Literal["all", "include", "a", "mx", "ptr", "ip4", "ip6", "exists"]


class Directive(BaseModel):
    qualifier: Optional[DirectiveQualifier]
    mecanism: DirectiveMecanism
    data: Optional[str]

    def to_tuple(self) -> Tuple:
        return (self.qualifier, self.mecanism, self.data)

    def __str__(self):
        data = f":{self.data}" if self.data else ""
        return f"{self.qualifier or ''}{self.mecanism}{data}"

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Directive):
            raise NotImplementedError()
        return self.to_tuple() == value.to_tuple()


class Modifier(BaseModel):
    name: str
    data: str

    def to_tuple(self) -> Tuple:
        return (self.name, self.data)

    def __str__(self):
        return f"{self.name}={self.data}"

    def __hash__(self) -> int:
        return hash(self.to_tuple())

    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Modifier):
            raise NotImplementedError()
        return self.to_tuple() == value.to_tuple()


class SPF(BaseModel):
    version: str = "spf1"
    terms: List[Union[Directive, Modifier]]

    @property
    def ignored(self):
        """
        From RFC: https://www.rfc-editor.org/rfc/rfc7208#section-5.1
            Mechanisms after "all" will never be tested.  Mechanisms listed after
            "all" MUST be ignored.  Any "redirect" modifier (Section 6.1) MUST be
            ignored when there is an "all" mechanism in the record, regardless of
            the relative ordering of the terms.
        """
        for i, t in enumerate(self.terms, 1):
            if t.mecanism == "all":
                return self.terms[i:]
        return []

    def __str__(self):
        return " ".join((f"v={self.version}", *(str(t) for t in self.terms)))

    def __repr__(self) -> str:
        return str(self)

    def __hash__(self) -> int:
        return hash((self.version, *tuple(self.terms)))


def is_spf(value):
    return value.lstrip().startswith(SPF_VERSION)


def split_spf(value):
    if not is_spf(value):
        raise Exception(f"Cannot split invalid SPF value: {value}")
    version, *terms = (p for p in (part.strip() for part in value.split(" ")) if p)
    if version != SPF_VERSION:
        raise Exception(
            f"SPF records must start with '{SPF_VERSION}'. Current value: {value}"
        )
    _tag, version = version.split("=")
    return version, terms


def parse_modifier(term):
    try:
        name, value = (t.strip() for t in term.split("=", 1))
    except Exception:
        logging.debug(term)
        raise
    return Modifier(
        name=name,
        data=value,
    )


def parse_directive(term):
    res = SPF_DIRECTIVE_REG.match(term)
    if not res:
        return None
    with_data = bool(res["with_data"])
    return Directive(
        qualifier=res["qualifier"] or None,
        mecanism=res["mecanism"].lower(),
        data=res["data"] if with_data else None,
    )


def parse_spf(value):
    version, raw_terms = split_spf(value)
    terms = []
    lookup_count = 0
    for t in raw_terms:
        directive = parse_directive(t)
        if directive:
            terms.append(directive)
            if directive.mecanism in MECANISMS_CAUSING_QUERIES:
                lookup_count += 1
            continue
        modifier = parse_modifier(t)
        if modifier.name in "redirect":
            lookup_count += 1
        terms.append(modifier)
    if lookup_count > LOOKUP_LIMIT:
        raise Exception(
            "Lookup limit exceeded according to RFC 7208, section 4.6.4: "
            "https://www.rfc-editor.org/rfc/rfc7208#section-4.6.4"
        )
    return SPF(
        version=version,
        terms=terms,
    )


def query_raw_spf(qname: str, raise_exception=False):
    try:
        answer = dns.resolver.resolve(qname, "TXT")
        values = [b"".join(x.strings).decode() for x in answer]
        return [x for x in values if is_spf(x)]
    # https://dnspython.readthedocs.io/en/latest/exceptions.html#dns-resolver-exceptions
    except dns.resolver.NoAnswer:  # dns.resolver.NXDOMAIN
        return []
    except Exception as e:
        if not raise_exception:
            logging.error(e)
            return None
        raise


def query_spf(qname: Optional[str], raise_exception=False):
    if qname is None:
        return []
    return [parse_spf(x) for x in query_raw_spf(qname, raise_exception=raise_exception)]


def recurse_spf(spf: SPF):
    """
    This function returns SPF records retrieve from recursive
    'includes' directives. The 'includes' directives are removed
    from the returned SPF records.

    NOTE: https://www.rfc-editor.org/rfc/rfc7208#section-5.2

    """
    terms: List[Union[Directive, Modifier]] = []
    includes: List[Directive] = []
    for t in spf.terms:
        if not isinstance(t, Directive):
            terms.append(t)
            continue
        if t.mecanism != "include" or t.data is None:
            terms.append(t)
            continue
        includes.append(t)
    yield SPF(
        version=spf.version,
        terms=terms,
    )
    for t in includes:
        for s in query_spf(t.data):
            yield from recurse_spf(s)


# def _resolve_spf_terms(spf: SPF):
#     for t in spf.terms:
#         if not isinstance(t, Directive):
#             yield t
#             continue
#         if t.mecanism != "include":
#             yield t
#             continue
#         spfs = query_spf(t.data)
#         for s in spfs:
#             yield from _resolve_spf_terms(s)

# def resolve_spf(spf: SPF):
#     return SPF(
#         version=spf.version,
#         terms=_resolve_spf_terms(spf)
#     )

__all__ = [
    "Directive",
    "Modifier",
    "SPF",
]
