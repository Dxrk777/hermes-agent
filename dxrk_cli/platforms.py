"""
Shared platform registry for Hermes Agent.

Single source of truth for platform metadata consumed by both
skills_config (label display) and tools_config (default toolset
resolution).  Import ``PLATFORMS`` from here instead of maintaining
duplicate dicts in each module.
"""

from collections import OrderedDict
from typing import NamedTuple


class PlatformInfo(NamedTuple):
    """Metadata for a single platform entry."""
    label: str
    default_toolset: str


# Ordered so that TUI menus are deterministic.
PLATFORMS: OrderedDict[str, PlatformInfo] = OrderedDict([
    ("cli",            PlatformInfo(label="🖥️  CLI",            default_toolset="dxrk-cli")),
    ("telegram",       PlatformInfo(label="📱 Telegram",        default_toolset="dxrk-telegram")),
    ("discord",        PlatformInfo(label="💬 Discord",         default_toolset="dxrk-discord")),
    ("slack",          PlatformInfo(label="💼 Slack",           default_toolset="dxrk-slack")),
    ("whatsapp",       PlatformInfo(label="📱 WhatsApp",        default_toolset="dxrk-whatsapp")),
    ("signal",         PlatformInfo(label="📡 Signal",          default_toolset="dxrk-signal")),
    ("bluebubbles",    PlatformInfo(label="💙 BlueBubbles",     default_toolset="dxrk-bluebubbles")),
    ("email",          PlatformInfo(label="📧 Email",           default_toolset="dxrk-email")),
    ("homeassistant",  PlatformInfo(label="🏠 Home Assistant",  default_toolset="dxrk-homeassistant")),
    ("mattermost",     PlatformInfo(label="💬 Mattermost",      default_toolset="dxrk-mattermost")),
    ("matrix",         PlatformInfo(label="💬 Matrix",          default_toolset="dxrk-matrix")),
    ("dingtalk",       PlatformInfo(label="💬 DingTalk",        default_toolset="dxrk-dingtalk")),
    ("feishu",         PlatformInfo(label="🪽 Feishu",          default_toolset="dxrk-feishu")),
    ("wecom",          PlatformInfo(label="💬 WeCom",           default_toolset="dxrk-wecom")),
    ("wecom_callback", PlatformInfo(label="💬 WeCom Callback",  default_toolset="dxrk-wecom-callback")),
    ("weixin",         PlatformInfo(label="💬 Weixin",          default_toolset="dxrk-weixin")),
    ("qqbot",          PlatformInfo(label="💬 QQBot",           default_toolset="dxrk-qqbot")),
    ("yuanbao",        PlatformInfo(label="🤖 Yuanbao",         default_toolset="dxrk-yuanbao")),
    ("webhook",        PlatformInfo(label="🔗 Webhook",         default_toolset="dxrk-webhook")),
    ("api_server",     PlatformInfo(label="🌐 API Server",      default_toolset="dxrk-api-server")),
    ("cron",           PlatformInfo(label="⏰ Cron",            default_toolset="dxrk-cron")),
])


def platform_label(key: str, default: str = "") -> str:
    """Return the display label for a platform key, or *default*."""
    info = PLATFORMS.get(key)
    return info.label if info is not None else default
