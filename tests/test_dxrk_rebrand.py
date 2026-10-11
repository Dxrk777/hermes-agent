"""Tests for the Hermes → Dxrk rebrand: DXRK_* canonical, HERMES_* fallback."""

import importlib.util
import os
import sys
from pathlib import Path

import pytest

import dxrk_constants
import hermes_constants
from dxrk_constants import (
    dxrk_getenv,
    dxrk_setenv,
    dxrk_unsetenv,
    get_default_dxrk_root,
    get_dxrk_home,
)


class TestDxrkHomeCanonical:
    def test_dxrk_home_wins_over_hermes_home(self, tmp_path, monkeypatch):
        monkeypatch.setenv("DXRK_HOME", str(tmp_path / "dxrk"))
        monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
        assert get_dxrk_home() == tmp_path / "dxrk"

    def test_hermes_home_fallback(self, tmp_path, monkeypatch):
        monkeypatch.delenv("DXRK_HOME", raising=False)
        monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
        assert get_dxrk_home() == tmp_path / "hermes"

    def test_default_when_neither_set(self, tmp_path, monkeypatch):
        monkeypatch.delenv("DXRK_HOME", raising=False)
        monkeypatch.delenv("HERMES_HOME", raising=False)
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        assert get_dxrk_home() == tmp_path / ".dxrk"


class TestDxrkGetenv:
    def test_canonical_wins(self, monkeypatch):
        monkeypatch.setenv("DXRK_REBRAND_PROBE", "dxrk")
        monkeypatch.setenv("HERMES_REBRAND_PROBE", "hermes")
        assert dxrk_getenv("DXRK_REBRAND_PROBE") == "dxrk"

    def test_legacy_fallback(self, monkeypatch):
        monkeypatch.delenv("DXRK_REBRAND_PROBE", raising=False)
        monkeypatch.setenv("HERMES_REBRAND_PROBE", "hermes")
        assert dxrk_getenv("DXRK_REBRAND_PROBE") == "hermes"

    def test_default(self, monkeypatch):
        monkeypatch.delenv("DXRK_REBRAND_PROBE", raising=False)
        monkeypatch.delenv("HERMES_REBRAND_PROBE", raising=False)
        assert dxrk_getenv("DXRK_REBRAND_PROBE", "dflt") == "dflt"
        assert dxrk_getenv("DXRK_REBRAND_PROBE") is None

    def test_empty_canonical_falls_through(self, monkeypatch):
        monkeypatch.setenv("DXRK_REBRAND_PROBE", "")
        monkeypatch.setenv("HERMES_REBRAND_PROBE", "hermes")
        assert dxrk_getenv("DXRK_REBRAND_PROBE") == "hermes"


class TestDxrkSetenv:
    def test_mirror(self, monkeypatch):
        monkeypatch.delenv("DXRK_REBRAND_PROBE", raising=False)
        monkeypatch.delenv("HERMES_REBRAND_PROBE", raising=False)
        dxrk_setenv("DXRK_REBRAND_PROBE", "1")
        try:
            assert os.environ["DXRK_REBRAND_PROBE"] == "1"
            assert os.environ["HERMES_REBRAND_PROBE"] == "1"
        finally:
            dxrk_unsetenv("DXRK_REBRAND_PROBE")
        assert "DXRK_REBRAND_PROBE" not in os.environ
        assert "HERMES_REBRAND_PROBE" not in os.environ


class TestDefaultRootCanonical:
    def test_dxrk_home_docker_root(self, tmp_path, monkeypatch):
        docker_home = tmp_path / "opt" / "data"
        docker_home.mkdir(parents=True)
        monkeypatch.setattr(Path, "home", lambda: tmp_path)
        monkeypatch.setenv("DXRK_HOME", str(docker_home))
        monkeypatch.setenv("HERMES_HOME", str(tmp_path / "other"))
        assert get_default_dxrk_root() == docker_home


class TestLegacyShims:
    def test_constants_shim_identity(self):
        assert hermes_constants.get_dxrk_home is dxrk_constants.get_dxrk_home
        assert hermes_constants.get_hermes_home is dxrk_constants.get_dxrk_home
        assert hermes_constants.dxrk_getenv is dxrk_constants.dxrk_getenv

    def test_logging_shim_identity(self):
        import dxrk_logging
        import hermes_logging

        assert hermes_logging.setup_logging is dxrk_logging.setup_logging

    def test_state_shim_identity(self):
        import dxrk_state
        import hermes_state

        assert hermes_state.SessionDB is dxrk_state.SessionDB

    def test_time_shim_identity(self):
        import dxrk_time
        import hermes_time

        assert hermes_time.now is dxrk_time.now


class TestSessionContextCanonical:
    def test_var_map_has_canonical_and_legacy(self):
        from gateway.session_context import _VAR_MAP

        for key in (
            "DXRK_SESSION_PLATFORM",
            "DXRK_SESSION_CHAT_ID",
            "DXRK_SESSION_KEY",
            "DXRK_CRON_AUTO_DELIVER_PLATFORM",
            "DXRK_CRON_AUTO_DELIVER_CHAT_ID",
            "DXRK_CRON_AUTO_DELIVER_THREAD_ID",
            "HERMES_SESSION_PLATFORM",
            "HERMES_SESSION_KEY",
            "HERMES_CRON_AUTO_DELIVER_PLATFORM",
        ):
            assert key in _VAR_MAP, key
        # Aliases resolve to the same ContextVar objects.
        assert _VAR_MAP["DXRK_SESSION_PLATFORM"] is _VAR_MAP["HERMES_SESSION_PLATFORM"]
        assert (
            _VAR_MAP["DXRK_CRON_AUTO_DELIVER_PLATFORM"]
            is _VAR_MAP["HERMES_CRON_AUTO_DELIVER_PLATFORM"]
        )

    def test_get_session_env_dxrk_wins(self, monkeypatch):
        from gateway.session_context import get_session_env

        monkeypatch.setenv("DXRK_SESSION_PLATFORM", "discord")
        monkeypatch.setenv("HERMES_SESSION_PLATFORM", "telegram")
        assert get_session_env("DXRK_SESSION_PLATFORM") == "discord"
        assert get_session_env("HERMES_SESSION_PLATFORM") == "discord"

    def test_get_session_env_legacy_fallback(self, monkeypatch):
        from gateway.session_context import get_session_env

        monkeypatch.delenv("DXRK_SESSION_PLATFORM", raising=False)
        monkeypatch.setenv("HERMES_SESSION_PLATFORM", "telegram")
        assert get_session_env("DXRK_SESSION_PLATFORM") == "telegram"
        assert get_session_env("HERMES_SESSION_PLATFORM") == "telegram"

    def test_contextvar_beats_environ(self, monkeypatch):
        from gateway.session_context import (
            clear_session_vars,
            get_session_env,
            set_session_vars,
        )

        tokens = set_session_vars(platform="ctx")
        try:
            monkeypatch.setenv("DXRK_SESSION_PLATFORM", "discord")
            assert get_session_env("DXRK_SESSION_PLATFORM") == "ctx"
            assert get_session_env("HERMES_SESSION_PLATFORM") == "ctx"
        finally:
            clear_session_vars(tokens)


class TestDxrkTimezone:
    def _reset_cache(self, monkeypatch):
        import dxrk_time

        monkeypatch.setattr(dxrk_time, "_cache_resolved", False)
        monkeypatch.setattr(dxrk_time, "_cached_tz", None)
        monkeypatch.setattr(dxrk_time, "_cached_tz_name", None)

    def test_dxrk_timezone_wins(self, monkeypatch):
        import dxrk_time

        self._reset_cache(monkeypatch)
        monkeypatch.setenv("DXRK_TIMEZONE", "Asia/Kolkata")
        monkeypatch.setenv("HERMES_TIMEZONE", "America/New_York")
        assert dxrk_time._resolve_timezone_name() == "Asia/Kolkata"

    def test_hermes_timezone_fallback(self, monkeypatch):
        import dxrk_time

        self._reset_cache(monkeypatch)
        monkeypatch.delenv("DXRK_TIMEZONE", raising=False)
        monkeypatch.setenv("HERMES_TIMEZONE", "Asia/Kolkata")
        assert dxrk_time._resolve_timezone_name() == "Asia/Kolkata"


class TestGetEnvValueBidirectional:
    def test_dxrk_key_reads_legacy_env(self, monkeypatch):
        from dxrk_cli.config import get_env_value

        monkeypatch.delenv("DXRK_REBRAND_PROBE", raising=False)
        monkeypatch.setenv("HERMES_REBRAND_PROBE", "legacy-val")
        assert get_env_value("DXRK_REBRAND_PROBE") == "legacy-val"

    def test_dxrk_key_prefers_canonical(self, monkeypatch):
        from dxrk_cli.config import get_env_value

        monkeypatch.setenv("DXRK_REBRAND_PROBE", "dxrk-val")
        monkeypatch.setenv("HERMES_REBRAND_PROBE", "legacy-val")
        assert get_env_value("DXRK_REBRAND_PROBE") == "dxrk-val"


class TestEnvVarEnabledFallback:
    def test_dxrk_name_reads_hermes(self, monkeypatch):
        from utils import env_var_enabled

        monkeypatch.delenv("DXRK_REBRAND_PROBE", raising=False)
        monkeypatch.setenv("HERMES_REBRAND_PROBE", "1")
        assert env_var_enabled("DXRK_REBRAND_PROBE") is True

    def test_hermes_name_reads_dxrk(self, monkeypatch):
        from utils import env_var_enabled

        monkeypatch.setenv("DXRK_REBRAND_PROBE", "yes")
        monkeypatch.delenv("HERMES_REBRAND_PROBE", raising=False)
        assert env_var_enabled("HERMES_REBRAND_PROBE") is True


class TestSkillHomeHelper:
    def _load_helper(self):
        path = (
            Path(__file__).parent.parent
            / "skills"
            / "productivity"
            / "google-workspace"
            / "scripts"
            / "_dxrk_home.py"
        )
        spec = importlib.util.spec_from_file_location("_dxrk_home_probe", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def test_dxrk_home_wins(self, monkeypatch, tmp_path):
        monkeypatch.setenv("DXRK_HOME", str(tmp_path / "dxrk"))
        monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
        mod = self._load_helper()
        assert mod.get_dxrk_home() == tmp_path / "dxrk"

    def test_hermes_home_fallback_without_dxrk_constants(self, monkeypatch, tmp_path):
        """Pure-stdlib fallback branch honors DXRK_HOME, then HERMES_HOME."""
        monkeypatch.setitem(sys.modules, "dxrk_constants", None)
        for name in list(sys.modules):
            if name.startswith("_dxrk_home"):
                del sys.modules[name]
        monkeypatch.setenv("DXRK_HOME", str(tmp_path / "dxrk"))
        monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes"))
        mod = self._load_helper()
        assert mod.get_dxrk_home() == tmp_path / "dxrk"
        monkeypatch.delenv("DXRK_HOME")
        for name in list(sys.modules):
            if name.startswith("_dxrk_home"):
                del sys.modules[name]
        mod = self._load_helper()
        assert mod.get_dxrk_home() == tmp_path / "hermes"
