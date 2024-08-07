import json
from typing import Any, Callable


def pprint(
    data: Any, *, indent: int = 2, default: Callable[[Any], str] = str
) -> str:
    return json.dumps(data, indent=indent, default=default)
