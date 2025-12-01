"""Plugin infrastructure module."""
from app.infrastructure.plugin.base_plugin import BasePlugin, OutputPlugin, InputPlugin, ProcessingPlugin
from app.infrastructure.plugin.plugin_loader import PluginLoader

__all__ = [
    "BasePlugin",
    "OutputPlugin",
    "InputPlugin",
    "ProcessingPlugin",
    "PluginLoader",
]

