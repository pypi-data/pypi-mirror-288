from typing import Generator, Tuple

MAX_DEPTH = 2**64


def max_depth(depth):
    if depth < 0:
        depth = MAX_DEPTH
    return range(depth)


# https://www.rfc-editor.org/rfc/rfc6376#section-3.2
# https://www.rfc-editor.org/rfc/rfc7489#section-6.3
# https://stackoverflow.com/questions/42531143/how-to-type-hint-a-generator-in-python-3
def parse_tag_value(value) -> Generator[Tuple[str, str], None, None]:
    yield from (
        (t.strip(), v.strip()) for t, v in (t.split("=", 1) for t in value.split(";"))
    )
