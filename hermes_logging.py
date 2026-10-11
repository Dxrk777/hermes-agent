"""Deprecated legacy alias for :mod:`dxrk_logging`.

The canonical implementation lives in :mod:`dxrk_logging`.  This module
exists only so ``import hermes_logging`` / ``from hermes_logging import ...``
(legacy) keep resolving to the same objects.  New code must import from
:mod:`dxrk_logging`.
"""

from dxrk_logging import *  # noqa: F401,F403
import dxrk_logging as _src
import sys as _sys

_mod = _sys.modules[__name__]
for _name in dir(_src):
    if _name.startswith("__") and _name not in ("__version__",):
        continue
    if not hasattr(_mod, _name):
        setattr(_mod, _name, getattr(_src, _name))

del _src, _sys, _mod, _name
