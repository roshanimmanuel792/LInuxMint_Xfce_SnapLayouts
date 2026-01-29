"""Window snapping engine using xdotool and wmctrl."""

import subprocess
import logging
import re
from typing import Tuple, Optional
from .monitor import Monitor

logger = logging.getLogger(__name__)


class WindowInfo:
    """Information about an X11 window."""
    
    def __init__(self, window_id: int, name: str, x: int, y: int, width: int, height: int, 
                 is_maximized: bool = False):
        self.window_id = window_id
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.is_maximized = is_maximized
    
    def __repr__(self):
        return f"WindowInfo(id={self.window_id:x}, name={self.name}, {self.width}x{self.height}+{self.x}+{self.y})"


class SnapEngine:
    """Handles window snapping operations."""
    
    def __init__(self):
        pass
    
    def get_active_window(self) -> Optional[WindowInfo]:
        """Get information about the currently active window."""
        try:
            # Get active window ID using xdotool
            result = subprocess.run(['xdotool', 'getactivewindow'], 
                                  capture_output=True, text=True, check=True)
            window_id = int(result.stdout.strip())
            
            if window_id <= 0:
                return None
            
            return self._get_window_info(window_id)
        except Exception as e:
            logger.error(f"Error getting active window: {e}")
            return None
    
    def _get_window_info(self, window_id: int) -> Optional[WindowInfo]:
        """Get information about a specific window."""
        try:
            # Get window name
            name_result = subprocess.run(['xdotool', 'getwindowname', str(window_id)],
                                        capture_output=True, text=True, check=True)
            name = name_result.stdout.strip()
            
            # Get window geometry
            geom_result = subprocess.run(['xdotool', 'getwindowgeometry', str(window_id)],
                                        capture_output=True, text=True, check=True)
            
            # Parse geometry output
            # Format: Position: 100,200 (screen: 0)
            #         Geometry: 800x600+100+200
            x, y, width, height = self._parse_window_geometry(geom_result.stdout)
            
            # Check if window is maximized (simple heuristic)
            is_maximized = self._is_window_maximized(window_id)
            
            return WindowInfo(window_id, name, x, y, width, height, is_maximized)
        except Exception as e:
            logger.error(f"Error getting window info for {window_id:x}: {e}")
            return None
    
    @staticmethod
    def _parse_window_geometry(geom_output: str) -> Tuple[int, int, int, int]:
        """Parse xdotool window geometry output."""
        try:
            for line in geom_output.split('\n'):
                if 'Geometry:' in line:
                    # Extract from "Geometry: 800x600+100+200"
                    match = re.search(r'(\d+)x(\d+)\+(-?\d+)\+(-?\d+)', line)
                    if match:
                        width, height, x, y = map(int, match.groups())
                        return x, y, width, height
            
            # Fallback
            return 0, 0, 800, 600
        except Exception as e:
            logger.error(f"Error parsing geometry: {e}")
            return 0, 0, 800, 600
    
    @staticmethod
    def _is_window_maximized(window_id: int) -> bool:
        """Check if window is maximized using xprop."""
        try:
            result = subprocess.run(['xprop', '-id', str(window_id), '_NET_WM_STATE'],
                                  capture_output=True, text=True, timeout=2)
            return '_NET_WM_STATE_MAXIMIZED' in result.stdout
        except Exception:
            return False
    
    def unmaximize_window(self, window_id: int) -> bool:
        """Remove maximized state from a window."""
        try:
            # Use wmctrl to unmaximize
            subprocess.run(['wmctrl', '-i', '-b', 'remove,maximized_vert,maximized_horz', 
                          '-r', f'0x{window_id:x}'],
                          check=False, capture_output=True)
            logger.info(f"Unmaximized window {window_id:x}")
            return True
        except Exception as e:
            logger.error(f"Error unmaximizing window: {e}")
            return False
    
    def snap_window(self, window_id: int, x: int, y: int, width: int, height: int) -> bool:
        """
        Snap a window to the given geometry.
        
        Args:
            window_id: X11 window ID
            x: Target X position
            y: Target Y position
            width: Target width
            height: Target height
        
        Returns:
            True if successful, False otherwise
        """
        try:
            logger.info(f"Snapping window {window_id:x} to {width}x{height}+{x}+{y}")
            
            # First, ensure window is not maximized
            if self._is_window_maximized(window_id):
                self.unmaximize_window(window_id)
            
            # Resize and move using xdotool
            subprocess.run(['xdotool', 'windowsize', str(window_id), str(width), str(height)],
                          check=True, capture_output=True)
            subprocess.run(['xdotool', 'windowmove', str(window_id), str(x), str(y)],
                          check=True, capture_output=True)
            
            # Restore focus
            subprocess.run(['xdotool', 'windowfocus', str(window_id)],
                          check=True, capture_output=True)
            
            logger.info(f"Successfully snapped window {window_id:x}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Error snapping window: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during snapping: {e}")
            return False
    
    def snap_active_window_to_zone(self, x: int, y: int, width: int, height: int) -> bool:
        """Snap the currently active window to the specified zone."""
        active_window = self.get_active_window()
        
        if not active_window:
            logger.warning("No active window found")
            return False
        
        return self.snap_window(active_window.window_id, x, y, width, height)


# Global snap engine instance
snap_engine = SnapEngine()
