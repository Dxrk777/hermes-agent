"""Canonical dxrk logging module (rename of hermes_logging).

Shim re-exporting hermes_logging so ``from dxrk_logging import ...`` works.
"""

from hermes_logging import *  # noqa: F401,F403
import hermes_logging as _src
import sys as _sys

_mod = _sys.modules[__name__]
for _name in dir(_src):
    if _name.startswith("__") and _name not in ("__version__",):
        continue
    if not hasattr(_mod, _name):
        setattr(_mod, _name, getattr(_src, _name))

del _src, _sys, _mod, _name
