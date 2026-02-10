#!/usr/bin/env python3
"""Test snapping on VS Code."""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xfce_snap_layouts.core import snap_engine

# Get active window (VS Code)
active = snap_engine.get_active_window()
if not active:
    print("No active window")
    sys.exit(1)

print(f"Active: {active.name}")
print(f"Before: {active.width}x{active.height}+{active.x}+{active.y}")

# Snap to left half
print("\nSnapping to LEFT (640x800+0+0)...")
success = snap_engine.snap_window(active.window_id, 0, 0, 640, 800)
print(f"Success: {success}")

time.sleep(0.5)

# Check result
after = snap_engine._get_window_info(active.window_id)
if after:
    print(f"After: {after.width}x{after.height}+{after.x}+{after.y}")
    if after.width == 640 and after.height == 800 and after.x == 0 and after.y == 0:
        print("✓ LEFT snap SUCCESSFUL!")
    else:
        print("✗ LEFT snap FAILED")

time.sleep(2)

# Snap to right half
print("\nSnapping to RIGHT (640x800+640+0)...")
success = snap_engine.snap_window(active.window_id, 640, 0, 640, 800)
print(f"Success: {success}")

time.sleep(0.5)

# Check result
after = snap_engine._get_window_info(active.window_id)
if after:
    print(f"After: {after.width}x{after.height}+{after.x}+{after.y}")
    if after.width == 640 and after.height == 800 and after.x == 640 and after.y == 0:
        print("✓ RIGHT snap SUCCESSFUL!")
    else:
        print("✗ RIGHT snap FAILED")
