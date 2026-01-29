"""Utilities package for xfce-snap-layouts."""

from .config import config_manager, ConfigManager
from .logger import setup_logging

__all__ = ['config_manager', 'ConfigManager', 'setup_logging']
