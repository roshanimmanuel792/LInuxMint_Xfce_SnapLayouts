#!/usr/bin/env python3
"""Test window snapping visually."""

import subprocess
import time
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xfce_snap_layouts.core import snap_engine, monitor_manager

# Get monitors
monitors = monitor_manager.get_all_monitors()
print(f"Monitors: {monitors}")

if not monitors:
    print("No monitors!")
    sys.exit(1)

monitor = monitors[0]
print(f"Using: {monitor}")

# Open xfce4-terminal
print("\nOpening terminal...")
proc = subprocess.Popen(['xfce4-terminal'])
time.sleep(2)

# Get active window
active = snap_engine.get_active_window()
if not active:
    print("Failed to get active window")
    proc.terminate()
    sys.exit(1)

print(f"Active window: {active}")
print(f"  Position: +{active.x}+{active.y}")
print(f"  Size: {active.width}x{active.height}")

# Snap to left half
left_x = monitor.x
left_y = monitor.y
left_width = monitor.width // 2
left_height = monitor.height

print(f"\nSnapping to LEFT zone: {left_width}x{left_height}+{left_x}+{left_y}")
success = snap_engine.snap_window(active.window_id, left_x, left_y, left_width, left_height)
print(f"Success: {success}")

time.sleep(2)

print("\nVisually verify the window is filling the LEFT HALF of the screen.")
print("If yes, the fix is working! If not, it's still having issues.")
print("\nPress ENTER to snap to right half...")
input()

# Snap to right half
right_x = monitor.x + monitor.width // 2
right_y = monitor.y
right_width = monitor.width // 2
right_height = monitor.height

print(f"\nSnapping to RIGHT zone: {right_width}x{right_height}+{right_x}+{right_y}")
success = snap_engine.snap_window(active.window_id, right_x, right_y, right_width, right_height)
print(f"Success: {success}")

time.sleep(2)

print("\nVisually verify the window is filling the RIGHT HALF of the screen.")
print("Press ENTER to finish...")
input()

proc.terminate()
print("\nTest complete!")
