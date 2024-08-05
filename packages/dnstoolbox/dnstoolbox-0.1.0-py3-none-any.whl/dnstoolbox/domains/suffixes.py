"""
This file retrieve informations about the suffixes.
The sources are:
- https://publicsuffix.org/  (Contains an effective list of suffixes, like .co.uk or .com.au)
  "Please use this URL and have your app download the list no more than once per day."
- https://www.iana.org/domains/root/db (TXT format: https://data.iana.org/TLD/tlds-alpha-by-domain.txt). This one does not contain .com.au for example.
(Found here: https://stackoverflow.com/questions/14427817/list-of-all-top-level-domains)

We will be using the effective list of suffix
"""

from functools import lru_cache

# from cachetools import TTLCache, cached
from typing import List, Optional, Tuple

import requests

# SUFFIX_MAPPING = Annotated[Dict[str, "SUFFIX_MAPPING"]]  # type: ignore[misc]


# https://publicsuffix.org/list/
@lru_cache
def _raw_get_public_suffixes(timeout=None) -> str:
    """
    Retrieve the raw text content of a file that
    list  public effective suffixes.
    This list also contains domains like ".co.uk" or ".com.au"
    that can be bought from a registrar.
    """
    res = requests.get(
        "https://publicsuffix.org/list/public_suffix_list.dat", timeout=timeout
    )
    # Explicitly provide the encoding since it is given by the api
    return res.content.decode("utf-8")


@lru_cache
def get_public_suffixes() -> List[str]:
    """
    Return a list with all the effective suffixes.
    This list also contains domains like ".co.uk" or ".com.au".

    NOTE: The list is sorted alphabetically
    """
    data = _raw_get_public_suffixes()
    lines = (line.strip() for line in data.splitlines())
    lines = (line for line in lines if not line.startswith("//"))
    return sorted(lines)


@lru_cache
def _reverse_dict(suffixes: Optional[Tuple[str, ...]] = None):
    """
    Given a list of suffixes like [".co.uk", "blogspot.co.uk", ".com.au"],
    this function returns the following dict:
    {
        "uk": {
            "co": {
                "blogspot": {},
            },
        },
        "au": {
            "com": {},
        }
    }

    This is usded to kick suffix lookup for a domain.
    E.g. we can easily find that ".co.uk" is the TLD for "hello.world.co.uk"
    (and not ".world.co.uk" or ".uk")

    Params:
        suffixes
    """
    iterable = suffixes if suffixes else get_public_suffixes()
    result = {}
    for s in iterable:
        parts = s.split(".")[::-1]
        data = result
        for p in parts:
            data = data.setdefault(p, {})
    return result


def simple_find_suffix(
    domain: str, suffixes: Optional[List[str]] = None
) -> Optional[str]:
    """
    This function is usefull when you have domains like "mydomain.com.au".
    The real suffix is ".com.au" and not ".au"
    """
    if suffixes is None:
        suffixes = get_public_suffixes()
    domain = domain.strip().strip(".").lower()
    found = ""
    for s in suffixes:
        if domain.endswith(s) and s > found:
            # print(f"new found: {s}")
            found = s
    return found or None


def optimized_find_suffix(
    domain: str, suffixes: Optional[List[str]] = None
) -> Optional[str]:
    """
    This function is usefull when you have domains like "mydomain.com.au".
    The real suffix is ".com.au" and not ".au"
    """
    mapping = _reverse_dict(tuple(suffixes) if suffixes else None)
    parts = domain.strip().strip(".").lower().split(".")[::-1]
    result = []
    for p in parts:
        mapping = mapping.get(p)  # types: ignore
        if mapping is None:
            break
        result.append(p)
    if not result:
        return None
    return ".".join(result[::-1])


find_suffix = optimized_find_suffix


def get_organizational_name(domain: str, suffix: Optional[str] = None) -> Optional[str]:
    """
    Return the organizational domain
    i.e. The domain we actually buy to a registrar.
    """
    if not suffix:
        suffix = find_suffix(domain)
    if not suffix:
        return None
    parts = domain.lower().removesuffix(suffix).split(".")
    parts = [p.strip() for p in parts if p]
    base = parts[-1]
    return f"{base}.{suffix}"


def is_organizational_name(domain: str, suffix: Optional[str] = None) -> bool:
    """
    Return the organizational domain
    i.e. The domain we actually buy to a registrar.
    """
    return domain == get_organizational_name(domain, suffix)
