from . import cname, dkim, dmarc, spf
from .records import Record

__all__ = [
    "dkim",
    "dmarc",
    "Record",
    "spf",
]
