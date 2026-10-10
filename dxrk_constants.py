"""Canonical dxrk constants module (rename of hermes_constants).

Shim that re-exports everything from hermes_constants so both
``import dxrk_constants`` (new) and ``import hermes_constants`` (legacy)
resolve to the same implementation. The canonical definitions live in
hermes_constants.py; this module exists only to complete the
hermes->dxrk rename without breaking either import path.
"""

from hermes_constants import *  # noqa: F401,F403
import hermes_constants as _src
import sys as _sys

_mod = _sys.modules[__name__]
for _name in dir(_src):
    if _name.startswith("__") and _name not in ("__version__",):
        continue
    if not hasattr(_mod, _name):
        setattr(_mod, _name, getattr(_src, _name))

# Back-compat aliases: map any remaining hermes-named symbols to dxrk names
# (covers the case where hermes_constants still defines old names).
_aliases = {
    "get_hermes_home": "get_dxrk_home",
    "get_default_hermes_root": "get_default_dxrk_root",
    "get_hermes_dir": "get_dxrk_dir",
    "display_hermes_home": "display_dxrk_home",
}
for _old, _new in _aliases.items():
    if hasattr(_mod, _old) and not hasattr(_mod, _new):
        setattr(_mod, _new, getattr(_mod, _old))
    if hasattr(_mod, _new) and not hasattr(_mod, _old):
        setattr(_mod, _old, getattr(_mod, _new))

del _src, _sys, _mod, _name, _aliases, _old, _new
