"""Canonical dxrk time module (rename of hermes_time).

Shim re-exporting hermes_time so ``from dxrk_time import now`` works.
"""

from hermes_time import *  # noqa: F401,F403
import hermes_time as _src
import sys as _sys

_mod = _sys.modules[__name__]
for _name in dir(_src):
    if _name.startswith("__") and _name not in ("__version__",):
        continue
    if not hasattr(_mod, _name):
        setattr(_mod, _name, getattr(_src, _name))

del _src, _sys, _mod, _name
