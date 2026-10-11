"""Deprecated legacy alias for :mod:`dxrk_time`.

The canonical implementation lives in :mod:`dxrk_time` (``DXRK_TIMEZONE``
canonical, ``HERMES_TIMEZONE`` deprecated fallback).  This module exists
only so ``from hermes_time import now`` (legacy) keeps working.  New code
must import from :mod:`dxrk_time`.
"""

from dxrk_time import *  # noqa: F401,F403
import dxrk_time as _src
import sys as _sys

_mod = _sys.modules[__name__]
for _name in dir(_src):
    if _name.startswith("__") and _name not in ("__version__",):
        continue
    if not hasattr(_mod, _name):
        setattr(_mod, _name, getattr(_src, _name))

del _src, _sys, _mod, _name
