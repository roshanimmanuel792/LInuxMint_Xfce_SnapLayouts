"""Controller that ties UI and snapping logic together."""

import logging
from typing import Optional
from ..core import (
    snap_engine, layout_engine, monitor_manager, SnapEngine, 
    LayoutEngine, MonitorManager, LayoutZone
)
from .overlay import overlay_manager

logger = logging.getLogger(__name__)


class SnapLayoutController:
    """Controller coordinating the snap layout workflow."""
    
    def __init__(self, snap_engine_: SnapEngine = None, 
                 layout_engine_: LayoutEngine = None,
                 monitor_manager_: MonitorManager = None):
        self.snap_engine = snap_engine_ or snap_engine
        self.layout_engine = layout_engine_ or layout_engine
        self.monitor_manager = monitor_manager_ or monitor_manager
        self.current_layout_id: Optional[str] = "50_50_split"
    
    def show_layout_picker(self, layout_id: str = None) -> bool:
        """
        Show the snap layout picker overlay.
        
        This is the main entry point for the snap layout workflow.
        
        Args:
            layout_id: Layout to show. If None, uses current layout.
        
        Returns:
            True if overlay was shown, False otherwise
        """
        try:
            # Get active window to determine monitor
            active_window = self.snap_engine.get_active_window()
            if not active_window:
                logger.warning("No active window found")
                return False
            
            # Determine which monitor the window is on
            monitor = self.monitor_manager.get_monitor_for_window(
                active_window.x, active_window.y
            )
            logger.info(f"Active window on monitor: {monitor.name}")
            
            # Get layout
            layout_id = layout_id or self.current_layout_id
            zones_data = self.layout_engine.get_layout_zones_for_monitor(layout_id, monitor)
            
            if not zones_data:
                logger.error(f"No zones for layout {layout_id}")
                return False
            
            # Show overlay
            return overlay_manager.show_overlay(
                monitor.geometry,
                zones_data,
                on_zone_selected=self._on_zone_selected
            )
        except Exception as e:
            logger.error(f"Error showing layout picker: {e}")
            return False
    
    def _on_zone_selected(self, zone: LayoutZone) -> None:
        """Handle zone selection from overlay."""
        try:
            logger.info(f"Zone selected: {zone.name}")
            
            # Get active window again
            active_window = self.snap_engine.get_active_window()
            if not active_window:
                logger.warning("No active window found")
                return
            
            # Get monitor
            monitor = self.monitor_manager.get_monitor_for_window(
                active_window.x, active_window.y
            )
            
            # Calculate geometry for the zone
            geometry = self.layout_engine.calculate_zone_geometry(zone, monitor)
            x, y, width, height = geometry
            
            # Snap the window
            success = self.snap_engine.snap_window(active_window.window_id, x, y, width, height)
            
            if success:
                logger.info(f"Successfully snapped window to {zone.name}")
            else:
                logger.error(f"Failed to snap window to {zone.name}")
        except Exception as e:
            logger.error(f"Error in zone selection handler: {e}")
    
    def set_active_layout(self, layout_id: str) -> bool:
        """Set the active layout."""
        layout = self.layout_engine.get_layout(layout_id)
        if layout:
            self.current_layout_id = layout_id
            logger.info(f"Active layout set to: {layout_id}")
            return True
        else:
            logger.error(f"Layout not found: {layout_id}")
            return False
    
    def get_available_layouts(self):
        """Get list of available layouts."""
        return self.layout_engine.get_all_layouts()


# Global controller instance
controller = SnapLayoutController()
