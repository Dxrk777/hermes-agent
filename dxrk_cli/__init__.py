"""
Dxrk CLI - Unified command-line interface for Dxrk Agent.

Provides subcommands for:
- dxrk chat          - Interactive chat (same as ./dxrk)
- dxrk gateway       - Run gateway in foreground
- dxrk gateway start - Start gateway service
- dxrk gateway stop  - Stop gateway service
- dxrk setup         - Interactive setup wizard
- dxrk status        - Show status of all components
- dxrk cron          - Manage cron jobs
"""

from importlib.metadata import version as _pkg_version, PackageNotFoundError

try:
    __version__ = _pkg_version("dxrk-agent")
except PackageNotFoundError:
    __version__ = "0.0.0-dev"

__release_date__ = "2026.4.23"
