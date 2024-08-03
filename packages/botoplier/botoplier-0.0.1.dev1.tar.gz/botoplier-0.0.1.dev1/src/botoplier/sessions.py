from __future__ import annotations

from os import getenv, path

# XXX get proper settings facilities?
CACHE_HOME = getenv("XDG_CACHE_HOME", None) or path.expanduser(path.join("~", ".cache"))
SESSION_CACHE_DIR = path.join(CACHE_HOME, "botoplier")
