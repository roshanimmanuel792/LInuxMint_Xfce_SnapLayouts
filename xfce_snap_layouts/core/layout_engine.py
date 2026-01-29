"""Layout engine for calculating snap geometry."""

import logging
from typing import Dict, Tuple, List
from dataclasses import dataclass
from .monitor import Monitor

logger = logging.getLogger(__name__)


@dataclass
class LayoutZone:
    """Represents a zone in a layout where a window can snap."""
    name: str
    x: int
    y: int
    width: int
    height: int
    label: str
    
    def to_rect(self) -> Tuple[int, int, int, int]:
        """Convert to (x, y, width, height) tuple."""
        return (self.x, self.y, self.width, self.height)


class Layout:
    """Represents a snap layout with multiple zones."""
    
    def __init__(self, name: str, layout_id: str, zones: List[LayoutZone]):
        self.name = name
        self.layout_id = layout_id
        self.zones = zones
    
    def get_zones_for_monitor(self, monitor: Monitor) -> List[LayoutZone]:
        """Get zones scaled to the monitor's dimensions."""
        scaled_zones = []
        for zone in self.zones:
            # Zones are stored as relative coordinates
            scaled_zone = LayoutZone(
                name=zone.name,
                x=monitor.x + zone.x,
                y=monitor.y + zone.y,
                width=zone.width,
                height=zone.height,
                label=zone.label
            )
            scaled_zones.append(scaled_zone)
        return scaled_zones


class LayoutEngine:
    """Manages snap layouts."""
    
    def __init__(self):
        self.layouts: Dict[str, Layout] = {}
        self._register_default_layouts()
    
    def _register_default_layouts(self) -> None:
        """Register the default snap layouts."""
        
        # 50/50 Split
        split_50_zones = [
            LayoutZone("left", 0, 0, 960, 1080, "Left"),
            LayoutZone("right", 960, 0, 960, 1080, "Right")
        ]
        self.layouts["50_50_split"] = Layout("50/50 Split", "50_50_split", split_50_zones)
        
        # 1 Big + 2 Small
        big_2_small_zones = [
            LayoutZone("big", 0, 0, 1152, 1080, "Big (60%)"),
            LayoutZone("small_top", 1152, 0, 768, 540, "Small Top (40%)"),
            LayoutZone("small_bottom", 1152, 540, 768, 540, "Small Bottom (40%)")
        ]
        self.layouts["1_big_2_small"] = Layout("1 Big + 2 Small", "1_big_2_small", big_2_small_zones)
        
        # 3 Columns
        three_col_zones = [
            LayoutZone("left", 0, 0, 640, 1080, "Left (33%)"),
            LayoutZone("center", 640, 0, 640, 1080, "Center (33%)"),
            LayoutZone("right", 1280, 0, 640, 1080, "Right (33%)")
        ]
        self.layouts["3_columns"] = Layout("3 Columns", "3_columns", three_col_zones)
    
    def get_layout(self, layout_id: str) -> Layout:
        """Get a layout by ID."""
        return self.layouts.get(layout_id)
    
    def get_all_layouts(self) -> List[Layout]:
        """Get all available layouts."""
        return list(self.layouts.values())
    
    def calculate_zone_geometry(self, zone: LayoutZone, monitor: Monitor) -> Tuple[int, int, int, int]:
        """
        Calculate actual geometry for a zone relative to a monitor.
        
        Args:
            zone: Layout zone with relative coordinates (based on 1920x1080)
            monitor: Target monitor
        
        Returns:
            (x, y, width, height) in screen coordinates
        """
        # Scale from base resolution (1920x1080) to monitor dimensions
        scale_x = monitor.width / 1920
        scale_y = monitor.height / 1080
        
        x = monitor.x + int(zone.x * scale_x)
        y = monitor.y + int(zone.y * scale_y)
        width = int(zone.width * scale_x)
        height = int(zone.height * scale_y)
        
        return (x, y, width, height)
    
    def get_layout_zones_for_monitor(self, layout_id: str, monitor: Monitor) -> List[Tuple[LayoutZone, Tuple[int, int, int, int]]]:
        """
        Get all zones for a layout, scaled to a monitor.
        
        Returns:
            List of (zone, geometry) tuples where geometry is (x, y, width, height)
        """
        layout = self.get_layout(layout_id)
        if not layout:
            logger.warning(f"Layout {layout_id} not found")
            return []
        
        result = []
        for zone in layout.zones:
            geometry = self.calculate_zone_geometry(zone, monitor)
            result.append((zone, geometry))
        
        return result


# Global layout engine instance
layout_engine = LayoutEngine()
