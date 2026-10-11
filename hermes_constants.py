"""Deprecated legacy alias for :mod:`dxrk_constants`.

The canonical definitions live in :mod:`dxrk_constants` (``DXRK_*`` env
vars, with ``HERMES_*`` honored as a deprecated fallback).  This module
exists only so ``import hermes_constants`` (legacy) keeps resolving to
the same implementation.  New code must ``import dxrk_constants``.
"""

from dxrk_constants import *  # noqa: F401,F403
import dxrk_constants as _src
import sys as _sys

_mod = _sys.modules[__name__]
for _name in dir(_src):
    if _name.startswith("__") and _name not in ("__version__",):
        continue
    if not hasattr(_mod, _name):
        setattr(_mod, _name, getattr(_src, _name))

# Back-compat aliases: map any dxrk-named symbols to hermes names
# (covers importers of the pre-rename API).
_aliases = {
    "get_dxrk_home": "get_hermes_home",
    "get_default_dxrk_root": "get_default_hermes_root",
    "get_dxrk_dir": "get_hermes_dir",
    "display_dxrk_home": "display_hermes_home",
}
for _old, _new in _aliases.items():
    if hasattr(_mod, _old) and not hasattr(_mod, _new):
        setattr(_mod, _new, getattr(_mod, _old))
    if hasattr(_mod, _new) and not hasattr(_mod, _old):
        setattr(_mod, _old, getattr(_mod, _new))

del _src, _sys, _mod, _name, _aliases, _old, _new
