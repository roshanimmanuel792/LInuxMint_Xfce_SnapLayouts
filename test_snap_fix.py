#!/usr/bin/env python3
"""Test the window snapping fix."""

import sys
import os
import subprocess
import time

# Add to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xfce_snap_layouts.core import snap_engine, monitor_manager

def test_snap():
    """Test snapping a terminal window to screen zones."""
    
    # Open a terminal window
    print("Opening a terminal window...")
    terminal_proc = subprocess.Popen(['xfce4-terminal', '--geometry', '80x24+500+300'])
    
    # Give it time to open
    time.sleep(2)
    
    # Get monitors
    monitors = monitor_manager.get_all_monitors()
    print(f"Detected monitors: {monitors}")
    
    if not monitors:
        print("No monitors detected!")
        terminal_proc.terminate()
        return
    
    monitor = monitors[0]
    print(f"Using monitor: {monitor.name} ({monitor.width}x{monitor.height} at +{monitor.x}+{monitor.y})")
    
    # Get active window (the terminal we just opened)
    time.sleep(0.5)
    active_window = snap_engine.get_active_window()
    if not active_window:
        print("Failed to get active window")
        terminal_proc.terminate()
        return
    
    print(f"Active window: {active_window}")
    
    # Test snapping to left half
    left_x = monitor.x
    left_y = monitor.y
    left_width = monitor.width // 2
    left_height = monitor.height
    
    print(f"\nSnapping to LEFT: {left_width}x{left_height}+{left_x}+{left_y}")
    success = snap_engine.snap_window(active_window.window_id, left_x, left_y, left_width, left_height)
    print(f"Snap result: {success}")
    
    time.sleep(2)
    
    # Get window info after snapping
    window_after = snap_engine._get_window_info(active_window.window_id)
    if window_after:
        print(f"Window after snap: {window_after}")
        print(f"  Expected: {left_width}x{left_height}+{left_x}+{left_y}")
        print(f"  Got:      {window_after.width}x{window_after.height}+{window_after.x}+{window_after.y}")
    
    time.sleep(2)
    
    # Test snapping to right half
    right_x = monitor.x + monitor.width // 2
    right_y = monitor.y
    right_width = monitor.width // 2
    right_height = monitor.height
    
    print(f"\nSnapping to RIGHT: {right_width}x{right_height}+{right_x}+{right_y}")
    success = snap_engine.snap_window(active_window.window_id, right_x, right_y, right_width, right_height)
    print(f"Snap result: {success}")
    
    time.sleep(2)
    
    # Get window info after snapping
    window_after = snap_engine._get_window_info(active_window.window_id)
    if window_after:
        print(f"Window after snap: {window_after}")
        print(f"  Expected: {right_width}x{right_height}+{right_x}+{right_y}")
        print(f"  Got:      {window_after.width}x{window_after.height}+{window_after.x}+{window_after.y}")
    
    time.sleep(3)
    
    # Cleanup
    terminal_proc.terminate()
    print("\nTest complete!")

if __name__ == "__main__":
    test_snap()
