#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from xfce_snap_layouts.ui import controller

print("Showing overlay... Press Ctrl+C in terminal to stop")
print("Look for a transparent overlay with 3 layout boxes on your screen")
controller.show_layout_picker()
Gtk.main()
