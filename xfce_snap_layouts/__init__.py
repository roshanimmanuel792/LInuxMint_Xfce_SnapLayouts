"""xfce-snap-layouts - Windows 11-style snap layouts for XFCE."""

__version__ = "1.0.0"
__author__ = "XFCE Snap Layouts Contributors"
__description__ = "Lightweight snap layout utility for Linux Mint XFCE"

from .utils import config_manager, setup_logging
from .core import (
    monitor_manager, layout_engine, snap_engine, keyboard_hook_manager
)
from .ui import controller, overlay_manager

__all__ = [
    'config_manager', 'setup_logging',
    'monitor_manager', 'layout_engine', 'snap_engine', 'keyboard_hook_manager',
    'controller', 'overlay_manager'
]
