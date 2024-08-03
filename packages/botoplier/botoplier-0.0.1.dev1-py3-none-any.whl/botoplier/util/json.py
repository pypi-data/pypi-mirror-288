import json as std_json
import re
from typing import IO, Any


class JSONEncoder(std_json.JSONEncoder):
    """Versatile and permissive JSONEncoder.

    Will use the __json__() method of any object that provides one.

    Adds support for Dates, Times, Regexp Matches and Dataclass instances
    out of the box.
    """

    def default(self, obj):
        if hasattr(obj, "__json__"):
            return obj.__json__()
        if hasattr(obj, "isoformat"):
            return obj.isoformat()  # datetime and similar
        if isinstance(obj, re.Match):
            return dict(match=obj.group(), match_spans=[obj.span(i) for i in range(len(obj.groups()) + 1)], match_type="regex.Match", matches=obj.groups())
        if hasattr(obj, "__dataclass_fields__"):
            return obj.__dict__
        return super().encode(obj)


def dump(obj: Any, fp: IO[str], **kwargs):
    return std_json.dump(obj, fp, cls=JSONEncoder, **kwargs)


def dumps(obj: Any, **kwargs):
    return std_json.dumps(obj, cls=JSONEncoder, **kwargs)
