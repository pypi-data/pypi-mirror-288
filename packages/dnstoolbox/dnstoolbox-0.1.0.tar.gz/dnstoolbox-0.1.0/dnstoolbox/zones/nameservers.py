# from dataclasses import dataclass, field

import socket
from functools import lru_cache
from typing import List, Optional, Tuple, cast

import dns.name
import dns.resolver
from cachetools import TTLCache, cached

# The root servers is supposed to be a static list of 13 servers
# https://www.iana.org/domains/root/servers
# https://www.internic.net/domain/root.zone
# https://www.iana.org/domains/root/servers

# Nb: Prefer to retrieve this list dynamically
# See: get_root_nameservers
ROOT_NAMESERVERS = [
    ("a.root-servers.net", "198.41.0.4"),
    ("b.root-servers.net", "170.247.170.2"),
    ("c.root-servers.net", "192.33.4.12"),
    ("d.root-servers.net", "199.7.91.13"),
    ("e.root-servers.net", "192.203.230"),
    ("f.root-servers.net", "192.5.5.241"),
    ("g.root-servers.net", "192.112.36.4"),
    ("h.root-servers.net", "198.97.190.53"),
    ("i.root-servers.net", "192.36.148.17"),
    ("j.root-servers.net", "192.58.128.30"),
    ("k.root-servers.net", "193.0.14.129"),
    ("l.root-servers.net", "199.7.83.42"),
    ("m.root-servers.net", "202.12.27.33"),
]


def _resolver_key(
    resolver: Optional[dns.resolver.Resolver]
) -> Optional[Tuple[str, ...]]:
    """
    This function returns a key (aka an identifier)
    for the DNS Resolver instance.

    This is used for caching in order to reduce the
    number of queries (performance/prevent being blacklisted)
    """
    if resolver is None:
        return None
    nameservers = cast(List[str], resolver.nameservers)
    return tuple(sorted(nameservers))


@lru_cache
def getip(domain: str) -> Optional[str]:
    """
    Return the IP of a domain.
    If an error occurs (e.g. Domain is invalid),
    None is returned instead
    """
    # We use the native socket library instead of dnspython
    # This prevent using an invalid Resolver (e.g. invalid nameservers)
    try:
        return socket.gethostbyname(domain)
    except Exception:
        return None


def nameservers2ips(nameservers: List[str], filter: bool = True) -> List[Optional[str]]:
    """
    Take a list of domains and convert all of them to ip addresses
    Params:
        filter (bool): Remove None from the result before returning it.
    """
    ips = (getip(s) for s in nameservers)
    if filter:
        ips = (x for x in ips if x)
    return list(ips)  # type: ignore


def parse_answer_authority(answer: dns.resolver.Answer) -> Optional[List[str]]:
    """
    Parse a DNS answer and returns its autority as a list of string.
    If no autority is provided, None is returned instead
    """
    answer_authority = answer.response.authority
    if answer_authority is None:
        return None
    return [x.to_text().split()[0] for authority in answer_authority for x in authority]


def _parse_answer(answer: dns.resolver.Answer) -> List[str]:
    """
    This function tries to retrieve the NS records for a domain.
    If no records are found, it fallbacks on the autority servers.

    NOTE: This function is only used to retrieve the root servers!
    """
    if not answer.rrset:
        return parse_answer_authority(answer) or []
    return [r.to_text() for r in answer.rrset]


# def get_next_nameservers(qname: str, ns):
#     if ns == ".":
#         answer = dns.resolver.resolve(".", "NS")
#         return parse_answer(answer)
#     ns = getip(ns)
#     answer = dns.resolver.resolve(qname, "NS", search=False, source=ns)
#     return parse_answer(answer)


@lru_cache
def _get_root_nameservers() -> List[str]:
    """
    Dynamically retrieve the root nameservers for '.'
    """
    answer = dns.resolver.resolve(".", "NS")
    return _parse_answer(answer)


@lru_cache
def get_root_nameservers() -> List[Tuple[str, str]]:
    """
    Return a list of (domain, ip) for the root servers.
    This list should be static and should contain 13 elements
    """
    global ROOT_NAMESERVERS
    nameservers = _get_root_nameservers()
    ips: List[str] = cast(List[str], nameservers2ips(nameservers))
    if not isinstance(ROOT_NAMESERVERS, list):
        ROOT_NAMESERVERS = []
    ROOT_NAMESERVERS[:] = zip(nameservers, ips)
    return ROOT_NAMESERVERS


@lru_cache
def get_root_resolver() -> Tuple[dns.resolver.Resolver, List[str]]:
    """
    This function returns the root resolver
    (i.e. the resolver that contacts "." and its nameservers)
    """
    nameservers = _get_root_nameservers()
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = cast(List[str], nameservers2ips(nameservers))
    return resolver, nameservers


@cached(cache=TTLCache(maxsize=1024, ttl=600), key=lambda d, r: (d, _resolver_key(r)))
def next_resolver(
    domain, resolver=None
) -> Tuple[Optional[dns.resolver.Resolver], List[str]]:
    """
    Given a resolver, this function returns the next resolver in the DNS resolution chain.
    We use this function to resolve . -> com. -> mydomain.com.

    NOTE: if resolver is None, then it returns the root resolver.
    """
    if not resolver:
        return get_root_resolver()
    answer = resolver.resolve(domain, "NS", raise_on_no_answer=False)
    authorities = parse_answer_authority(answer)
    if not authorities:
        return None, []
    r = dns.resolver.Resolver(configure=False)
    r.nameservers = cast(List[str], nameservers2ips(authorities))
    return r, authorities


def resolve_authorities(domain: str, max_depth: int = 10) -> List[List[str]]:
    """
    This function returns all the autoritative servers implied to resolve domain.
    """
    results = []
    resolver = None
    previous_nameservers = set()
    for _ in range(max_depth):
        resolver, nameservers = next_resolver(domain, resolver)
        if not resolver:
            break
        ns_set = set(nameservers)
        if ns_set & previous_nameservers:
            break
        previous_nameservers = ns_set
        results.append(nameservers)
    return results


def get_authoritative_nameservers(domain: str) -> List[str]:
    """
    Return the list of authoritative nameservers for the domain.

    NOTE: This is very different than requesting the APEX NS records of the domain.
    (Even if the both results should ideally match)
    """
    chain = resolve_authorities(domain)
    if chain:
        return chain[-1]
    return []


__all__ = [
    "resolve_authorities",
    "get_authoritative_nameservers",
]
