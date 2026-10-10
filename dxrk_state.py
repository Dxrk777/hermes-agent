"""Canonical dxrk state module (rename of hermes_state).

Shim re-exporting hermes_state so ``from dxrk_state import SessionDB`` works.
"""

from hermes_state import *  # noqa: F401,F403
import hermes_state as _src
import sys as _sys

_mod = _sys.modules[__name__]
for _name in dir(_src):
    if _name.startswith("__") and _name not in ("__version__",):
        continue
    if not hasattr(_mod, _name):
        setattr(_mod, _name, getattr(_src, _name))

del _src, _sys, _mod, _name
