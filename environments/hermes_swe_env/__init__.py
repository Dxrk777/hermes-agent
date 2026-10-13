"""Deprecated shim — use environments.dxrk_swe_env instead."""
try:
    from environments.dxrk_swe_env.dxrk_swe_env import (
        DxrkSweEnv,
        DxrkSweEnvConfig,
        HermesSweEnv,
        HermesSweEnvConfig,
    )
    __all__ = ["DxrkSweEnv", "DxrkSweEnvConfig", "HermesSweEnv", "HermesSweEnvConfig"]
except ImportError:
    __all__ = []
