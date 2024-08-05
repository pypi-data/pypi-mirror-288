# from dataclasses import dataclass, field

import dns.name
import dns.resolver

# def resolve_cname(qname):
#     n = dns.name.from_text(qname)
#     try:
#         #On envoie une requête de type NS :
#         return dns.resolver.query(n, "CNAME")
#     except dns.resolver.NoAnswer:
#         return None


def _resolve_cname(qname):
    try:
        return dns.resolver.resolve(qname)
    except dns.resolver.NoAnswer:
        return None


def resolve_cname_chain(qname):
    answer = _resolve_cname(qname)
    if not answer:
        return None
    return answer.chaining_result.cnames


def resolve_cname(qname):
    answer = _resolve_cname(qname)
    if not answer:
        return None
    return [x.address for x in answer.rrset]


def find_ns_records(qname, allow_not_existing=True):
    n = dns.name.from_text(qname)
    ResponseException = dns.resolver.NoAnswer  # noqa
    if allow_not_existing:
        ResponseException = (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN)  # noqa
    while True:
        try:
            # We send a request for type NS :
            answer = dns.resolver.query(n, "NS")
            return n.to_text(), [r.target.to_text() for r in answer.rrset]
        except ResponseException:
            try:
                n = n.parent()
            except dns.name.NoParent:
                return None
