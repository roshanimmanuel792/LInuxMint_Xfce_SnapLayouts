"""Launcher and main entry point for xfce-snap-layouts."""

import sys
import signal
import logging
import time
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib
import subprocess

from xfce_snap_layouts.utils import setup_logging, config_manager
from xfce_snap_layouts.core import keyboard_hook_manager
from xfce_snap_layouts.ui import controller

logger = logging.getLogger(__name__)


class SnapLayoutDaemon:
    """Main daemon that listens for hotkeys and shows overlay."""
    
    def __init__(self):
        self.running = False
        self.hotkey_process = None
        self.config = config_manager
    
    def _setup_xbindkeys(self) -> bool:
        """Set up xbindkeys for global hotkey capture."""
        try:
            # Create xbindkeysrc content
            hotkey = self.config.get("keyboard_shortcut", "<Super>z")
            
            # Convert hotkey to xbindkeys format
            xbindkeys_cmd = self._convert_hotkey_to_xbindkeys(hotkey)
            
            logger.info(f"Setting up xbindkeys with: {xbindkeys_cmd}")
            return True
        except Exception as e:
            logger.error(f"Error setting up xbindkeys: {e}")
            return False
    
    @staticmethod
    def _convert_hotkey_to_xbindkeys(hotkey: str) -> str:
        """Convert hotkey format to xbindkeys format."""
        # Convert from <Super>z to mod4 + z
        hotkey = hotkey.replace("<Super>", "mod4")
        hotkey = hotkey.replace("<Alt>", "mod1")
        hotkey = hotkey.replace("<Control>", "control")
        hotkey = hotkey.replace("<Shift>", "shift")
        return hotkey
    
    def _on_hotkey_pressed(self) -> None:
        """Handle hotkey press."""
        logger.info("Hotkey pressed, showing overlay")
        try:
            # Show layout picker on the current layout
            controller.show_layout_picker()
        except Exception as e:
            logger.error(f"Error showing overlay: {e}")
    
    def _setup_signal_handlers(self) -> None:
        """Set up signal handlers for graceful shutdown."""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down")
            self.stop()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def start(self) -> bool:
        """Start the daemon."""
        try:
            logger.info("Starting xfce-snap-layouts daemon")
            self.running = True
            self._setup_signal_handlers()
            
            # Register hotkey
            hotkey = self.config.get("keyboard_shortcut", "<Super>z")
            keyboard_hook_manager.register_hotkey(hotkey, self._on_hotkey_pressed)
            keyboard_hook_manager.start()
            
            logger.info("Daemon started successfully")
            return True
        except Exception as e:
            logger.error(f"Error starting daemon: {e}")
            self.running = False
            return False
    
    def stop(self) -> None:
        """Stop the daemon."""
        if self.running:
            logger.info("Stopping daemon")
            self.running = False
            keyboard_hook_manager.stop()
    
    def run_gtk_loop(self) -> None:
        """Run the GTK main loop."""
        try:
            Gtk.main()
        except KeyboardInterrupt:
            logger.info("GTK loop interrupted")
            self.stop()


class SimpleHotkeyApp(Gtk.Application):
    """GTK Application that listens for hotkeys using an external tool."""
    
    def __init__(self):
        super().__init__()
        self.daemon = None
    
    def do_activate(self):
        """Activate the application."""
        # Create a hidden window (GTK apps need at least one window)
        window = Gtk.ApplicationWindow(application=self)
        window.set_default_size(1, 1)
        window.hide()
        window.set_skip_taskbar_hint(True)
        window.set_skip_pager_hint(True)
        
        self.daemon = SnapLayoutDaemon()
        self.daemon.start()
        
        # Set up periodic check for hotkey using xdotool
        GLib.timeout_add_seconds(1, self._check_hotkey)
    
    def _check_hotkey(self) -> bool:
        """Check if hotkey is pressed (using external command)."""
        if not self.daemon.running:
            return False
        
        try:
            # This is a simple implementation. In production, you'd want to use
            # a proper X11 event listener library
            hotkey_cmd = self.daemon.config.get("keyboard_shortcut", "<Super>z")
            # Trigger callback directly for testing
            # In real implementation, this would be triggered by xbindkeys or similar
        except Exception as e:
            logger.error(f"Error checking hotkey: {e}")
        
        return True


def main():
    """Main entry point."""
    # Set up logging
    log_level = logging.DEBUG
    setup_logging(log_level)
    logger.info("Starting xfce-snap-layouts")
    
    try:
        # Check dependencies
        if not _check_dependencies():
            logger.error("Missing required dependencies")
            return 1
        
        # Start the application
        app = SimpleHotkeyApp()
        exit_code = app.run(sys.argv)
        
        logger.info("Application exited")
        return exit_code
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1


def _check_dependencies() -> bool:
    """Check if required tools are available."""
    required_tools = ['xdotool', 'wmctrl', 'xrandr', 'xprop']
    
    for tool in required_tools:
        try:
            subprocess.run(['which', tool], capture_output=True, check=True)
            logger.debug(f"Found {tool}")
        except subprocess.CalledProcessError:
            logger.error(f"Missing required tool: {tool}")
            return False
    
    return True


if __name__ == '__main__':
    sys.exit(main())
