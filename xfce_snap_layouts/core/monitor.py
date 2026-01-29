"""Monitor detection and management using xrandr."""

import subprocess
import logging
from typing import List, Dict, Tuple
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class Monitor:
    """Represents a monitor with its geometry."""
    name: str
    x: int
    y: int
    width: int
    height: int
    is_primary: bool = False
    
    @property
    def geometry(self) -> Tuple[int, int, int, int]:
        """Return (x, y, width, height)."""
        return (self.x, self.y, self.width, self.height)
    
    def contains_point(self, px: int, py: int) -> bool:
        """Check if point (px, py) is within monitor bounds."""
        return (self.x <= px < self.x + self.width and 
                self.y <= py < self.y + self.height)


class MonitorManager:
    """Manages monitor detection and information."""
    
    def __init__(self):
        self.monitors: List[Monitor] = []
        self.primary_monitor: Monitor = None
        self._refresh_monitors()
    
    def _refresh_monitors(self) -> None:
        """Detect all monitors using xrandr."""
        try:
            result = subprocess.run(['xrandr'], capture_output=True, text=True, check=True)
            self.monitors = self._parse_xrandr_output(result.stdout)
            self.primary_monitor = next((m for m in self.monitors if m.is_primary), 
                                       self.monitors[0] if self.monitors else None)
            logger.info(f"Detected {len(self.monitors)} monitor(s)")
            for monitor in self.monitors:
                logger.debug(f"  {monitor.name}: {monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
        except Exception as e:
            logger.error(f"Error detecting monitors: {e}")
            self.monitors = []
            self.primary_monitor = None
    
    @staticmethod
    def _parse_xrandr_output(output: str) -> List[Monitor]:
        """Parse xrandr output to extract monitor information."""
        monitors = []
        lines = output.strip().split('\n')
        
        for line in lines:
            # Match connected monitors with geometry
            # Format: HDMI-1 connected primary 1920x1080+0+0
            parts = line.split()
            if len(parts) >= 2 and ('connected' in line or 'disconnected' in line):
                if 'disconnected' in line:
                    continue  # Skip disconnected monitors
                
                monitor_name = parts[0]
                is_primary = 'primary' in line
                
                # Find geometry part (contains +)
                for part in parts:
                    if '+' in part and 'x' in part:
                        try:
                            # Parse format: 1920x1080+0+0
                            geometry_part = part.split('+')
                            resolution = geometry_part[0].split('x')
                            width = int(resolution[0])
                            height = int(resolution[1])
                            x = int(geometry_part[1])
                            y = int(geometry_part[2])
                            
                            monitors.append(Monitor(
                                name=monitor_name,
                                x=x, y=y,
                                width=width, height=height,
                                is_primary=is_primary
                            ))
                            break
                        except (ValueError, IndexError) as e:
                            logger.warning(f"Could not parse geometry for {monitor_name}: {part}")
                            continue
        
        return monitors if monitors else [Monitor("default", 0, 0, 1920, 1080)]
    
    def get_monitor_for_window(self, window_x: int, window_y: int) -> Monitor:
        """Get the monitor containing the given window position."""
        for monitor in self.monitors:
            if monitor.contains_point(window_x, window_y):
                return monitor
        
        # Fallback to primary monitor
        if self.primary_monitor:
            return self.primary_monitor
        
        # Fallback to first monitor
        return self.monitors[0] if self.monitors else Monitor("default", 0, 0, 1920, 1080)
    
    def get_all_monitors(self) -> List[Monitor]:
        """Get list of all monitors."""
        return self.monitors
    
    def refresh(self) -> None:
        """Refresh monitor information."""
        self._refresh_monitors()


# Global monitor manager instance
monitor_manager = MonitorManager()
