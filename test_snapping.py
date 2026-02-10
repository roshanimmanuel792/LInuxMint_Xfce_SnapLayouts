#!/usr/bin/env python3
"""Test the snapping via overlay and verify windows fit properly."""

import sys
import os
import time
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from xfce_snap_layouts.ui.controller import SnapLayoutController
from xfce_snap_layouts.core import snap_engine, layout_engine, monitor_manager

def test_snapping():
    """Test snapping functionality."""
    
    print("=== Testing Window Snapping with wmctrl ===\n")
    
    # Open a terminal for testing
    print("1. Opening terminal window...")
    term = subprocess.Popen(['xfce4-terminal', '--geometry', '100x30+100+100'],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    
    # Get active window
    print("2. Getting active window...")
    active_window = snap_engine.get_active_window()
    if not active_window:
        print("ERROR: Could not get active window")
        term.terminate()
        return False
    
    print(f"   Window: {active_window.name}")
    print(f"   Current geometry: {active_window.width}x{active_window.height}+{active_window.x}+{active_window.y}")
    
    # Get monitor
    print("\n3. Getting monitor info...")
    monitors = monitor_manager.get_all_monitors()
    if not monitors:
        print("ERROR: No monitors found")
        term.terminate()
        return False
    
    monitor = monitors[0]
    print(f"   Monitor: {monitor.name}")
    print(f"   Resolution: {monitor.width}x{monitor.height}")
    
    # Test left zone
    print("\n4. Testing LEFT zone snap...")
    left_zone_x = monitor.x
    left_zone_y = monitor.y
    left_zone_width = monitor.width // 2
    left_zone_height = monitor.height
    
    print(f"   Target: {left_zone_width}x{left_zone_height}+{left_zone_x}+{left_zone_y}")
    success = snap_engine.snap_window(active_window.window_id, 
                                      left_zone_x, left_zone_y, 
                                      left_zone_width, left_zone_height)
    print(f"   Snap result: {success}")
    
    time.sleep(1)
    
    # Check result
    after = snap_engine._get_window_info(active_window.window_id)
    if after:
        print(f"   Actual: {after.width}x{after.height}+{after.x}+{after.y}")
        
        # Check if window is approximately in the right place
        width_ok = abs(after.width - left_zone_width) <= 2
        x_ok = abs(after.x - left_zone_x) <= 2
        y_ok = abs(after.y - left_zone_y) <= 2
        
        if width_ok and x_ok and y_ok:
            print("   ✓ LEFT snap SUCCESSFUL!")
        else:
            print("   ✗ LEFT snap failed - window not fitting correctly")
            print(f"     Width diff: {after.width} vs {left_zone_width} (ok={width_ok})")
            print(f"     X diff: {after.x} vs {left_zone_x} (ok={x_ok})")
            print(f"     Y diff: {after.y} vs {left_zone_y} (ok={y_ok})")
    
    time.sleep(1)
    
    # Test right zone
    print("\n5. Testing RIGHT zone snap...")
    right_zone_x = monitor.x + monitor.width // 2
    right_zone_y = monitor.y
    right_zone_width = monitor.width // 2
    right_zone_height = monitor.height
    
    print(f"   Target: {right_zone_width}x{right_zone_height}+{right_zone_x}+{right_zone_y}")
    success = snap_engine.snap_window(active_window.window_id,
                                      right_zone_x, right_zone_y,
                                      right_zone_width, right_zone_height)
    print(f"   Snap result: {success}")
    
    time.sleep(1)
    
    # Check result
    after = snap_engine._get_window_info(active_window.window_id)
    if after:
        print(f"   Actual: {after.width}x{after.height}+{after.x}+{after.y}")
        
        # Check if window is approximately in the right place
        width_ok = abs(after.width - right_zone_width) <= 2
        x_ok = abs(after.x - right_zone_x) <= 2
        y_ok = abs(after.y - right_zone_y) <= 2
        
        if width_ok and x_ok and y_ok:
            print("   ✓ RIGHT snap SUCCESSFUL!")
        else:
            print("   ✗ RIGHT snap failed - window not fitting correctly")
            print(f"     Width diff: {after.width} vs {right_zone_width} (ok={width_ok})")
            print(f"     X diff: {after.x} vs {right_zone_x} (ok={x_ok})")
            print(f"     Y diff: {after.y} vs {right_zone_y} (ok={y_ok})")
    
    time.sleep(2)
    
    # Cleanup
    term.terminate()
    print("\n=== Test Complete ===")
    return True

if __name__ == "__main__":
    try:
        test_snapping()
    except KeyboardInterrupt:
        print("\nTest interrupted")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
