"""GTK overlay UI for snap layouts."""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import logging
from typing import Callable, Optional, List, Tuple
from ..core import LayoutZone

logger = logging.getLogger(__name__)


class LayoutZoneButton(Gtk.EventBox):
    """A clickable zone in the layout overlay."""
    
    def __init__(self, zone: LayoutZone, geometry: Tuple[int, int, int, int], 
                 on_click: Optional[Callable] = None):
        super().__init__()
        self.zone = zone
        self.geometry = geometry
        self.on_click = on_click
        self.is_highlighted = False
        
        x, y, width, height = geometry
        self.set_size_request(width, height)
        
        # Create drawing area
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.connect("draw", self._on_draw)
        self.add(self.drawing_area)
        
        # Connect events
        self.connect("enter-notify-event", self._on_enter)
        self.connect("leave-notify-event", self._on_leave)
        self.connect("button-press-event", self._on_click)
        
        self.set_events(Gdk.EventMask.ENTER_NOTIFY_MASK | 
                       Gdk.EventMask.LEAVE_NOTIFY_MASK |
                       Gdk.EventMask.BUTTON_PRESS_MASK)
    
    def _on_draw(self, widget, cr):
        """Draw the zone."""
        x, y, width, height = self.geometry
        
        # Draw background
        if self.is_highlighted:
            # Highlight color (blue)
            cr.set_source_rgba(0.0, 0.47, 0.83, 0.3)
        else:
            # Transparent
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.1)
        
        cr.rectangle(0, 0, width, height)
        cr.fill()
        
        # Draw border
        cr.set_source_rgba(0.0, 0.47, 0.83, 0.6)
        cr.set_line_width(2)
        cr.rectangle(0, 0, width, height)
        cr.stroke()
        
        # Draw label
        if self.is_highlighted:
            cr.set_source_rgba(1.0, 1.0, 1.0, 1.0)
        else:
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.8)
        
        layout = Gtk.Widget.create_pango_layout(self, self.zone.label)
        font_desc = layout.get_context().get_font_description()
        font_desc.set_size(14 * 1024)  # Pango uses 1024ths of a point
        layout.set_font_description(font_desc)
        
        width_pango, height_pango = layout.get_pixel_size()
        x_label = (width - width_pango) // 2
        y_label = (height - height_pango) // 2
        
        cr.move_to(x_label, y_label)
        Gtk.render_layout(Gtk.StyleContext(), cr, x_label, y_label, layout)
    
    def _on_enter(self, widget, event):
        """Handle mouse enter."""
        self.is_highlighted = True
        self.drawing_area.queue_draw()
    
    def _on_leave(self, widget, event):
        """Handle mouse leave."""
        self.is_highlighted = False
        self.drawing_area.queue_draw()
    
    def _on_click(self, widget, event):
        """Handle click."""
        if self.on_click:
            self.on_click(self.zone)


class SnapLayoutOverlay(Gtk.Window):
    """Main overlay window displaying snap layouts."""
    
    def __init__(self, monitor_geom: Tuple[int, int, int, int],
                 zones_data: List[Tuple[LayoutZone, Tuple[int, int, int, int]]],
                 on_zone_selected: Optional[Callable] = None,
                 on_close: Optional[Callable] = None):
        super().__init__(Gtk.WindowType.POPUP)
        
        self.monitor_geom = monitor_geom
        self.zones_data = zones_data
        self.on_zone_selected = on_zone_selected
        self.on_close = on_close
        self.zone_buttons: List[LayoutZoneButton] = []
        
        # Window properties
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_accept_focus(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        
        # Set RGBA for transparency
        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.set_visual(visual)
        self.set_app_paintable(True)
        
        # Position and size window
        mx, my, mw, mh = monitor_geom
        self.set_default_size(mw, mh)
        self.move(mx, my)
        
        # Create layout
        self._setup_ui()
        
        # Connect signals
        self.connect("key-press-event", self._on_key_press)
        self.connect("focus-out-event", self._on_focus_out)
    
    def _setup_ui(self) -> None:
        """Set up the UI with zones."""
        # Fixed container to place zones at exact positions
        fixed = Gtk.Fixed()
        
        for zone, geometry in self.zones_data:
            x, y, width, height = geometry
            mx, my, _, _ = self.monitor_geom
            
            # Calculate relative position
            rel_x = x - mx
            rel_y = y - my
            
            button = LayoutZoneButton(zone, (rel_x, rel_y, width, height),
                                     on_click=self._on_zone_click)
            fixed.put(button, rel_x, rel_y)
            self.zone_buttons.append(button)
        
        self.add(fixed)
    
    def _on_zone_click(self, zone: LayoutZone) -> None:
        """Handle zone selection."""
        logger.info(f"Zone selected: {zone.name}")
        if self.on_zone_selected:
            self.on_zone_selected(zone)
        self.close()
    
    def _on_key_press(self, widget, event) -> bool:
        """Handle key press."""
        if event.keyval == Gdk.KEY_Escape:
            self.close()
            return True
        return False
    
    def _on_focus_out(self, widget, event) -> bool:
        """Handle focus out (close on focus loss)."""
        # Use idle to allow proper event processing
        GLib.idle_add(self.close)
        return False
    
    def close(self) -> None:
        """Close the overlay."""
        if self.on_close:
            self.on_close()
        self.destroy()


class OverlayManager:
    """Manages the overlay lifecycle."""
    
    def __init__(self):
        self.current_overlay: Optional[SnapLayoutOverlay] = None
    
    def show_overlay(self, monitor_geom: Tuple[int, int, int, int],
                    zones_data: List[Tuple[LayoutZone, Tuple[int, int, int, int]]],
                    on_zone_selected: Optional[Callable] = None) -> bool:
        """
        Show the snap layout overlay.
        
        Returns:
            True if overlay was shown, False if one is already open
        """
        if self.current_overlay:
            logger.warning("Overlay already open")
            return False
        
        try:
            def on_close():
                self.current_overlay = None
            
            self.current_overlay = SnapLayoutOverlay(
                monitor_geom, zones_data,
                on_zone_selected=on_zone_selected,
                on_close=on_close
            )
            
            self.current_overlay.show_all()
            logger.info("Overlay shown")
            return True
        except Exception as e:
            logger.error(f"Error showing overlay: {e}")
            self.current_overlay = None
            return False
    
    def hide_overlay(self) -> None:
        """Hide the current overlay."""
        if self.current_overlay:
            self.current_overlay.close()
            self.current_overlay = None


# Global overlay manager instance
overlay_manager = OverlayManager()
