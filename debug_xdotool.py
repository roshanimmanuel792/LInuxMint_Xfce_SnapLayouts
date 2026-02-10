#!/usr/bin/env python3
"""Debug xdotool window sizing."""

import subprocess
import time
import sys

# Get the active window
result = subprocess.run(['xdotool', 'getactivewindow'], capture_output=True, text=True)
window_id = result.stdout.strip()
print(f"Active window ID: {window_id}")

# Get current geometry
result = subprocess.run(['xdotool', 'getwindowgeometry', window_id], 
                       capture_output=True, text=True)
print(f"Current geometry:\n{result.stdout}")

# Try to resize
print("\nTrying to resize to 640x800...")
result = subprocess.run(['xdotool', 'windowsize', window_id, '640', '800'], 
                       capture_output=True, text=True)
if result.returncode != 0:
    print(f"Error: {result.stderr}")
else:
    print("Command succeeded")

time.sleep(1)

# Get new geometry
result = subprocess.run(['xdotool', 'getwindowgeometry', window_id], 
                       capture_output=True, text=True)
print(f"\nGeometry after resize:\n{result.stdout}")

# Try with wmctrl
print("\nTrying wmctrl approach...")
result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
print(f"wmctrl -l output:\n{result.stdout}")

# Use wmctrl to set geometry
print("\nUsing wmctrl to set geometry 640x800+0+0...")
result = subprocess.run(['wmctrl', '-r', ':ACTIVE:', '-b', 'add,maximized_vert,maximized_horz'],
                       capture_output=True, text=True)
print(f"Result: {result.returncode}")

time.sleep(0.5)

result = subprocess.run(['wmctrl', '-r', ':ACTIVE:', '-b', 'remove,maximized_vert,maximized_horz'],
                       capture_output=True, text=True)
print(f"Result: {result.returncode}")

time.sleep(0.5)

result = subprocess.run(['wmctrl', '-r', ':ACTIVE:', '-e', '0,0,0,640,800'],
                       capture_output=True, text=True)
if result.returncode != 0:
    print(f"wmctrl error: {result.stderr}")
else:
    print("wmctrl succeeded")

time.sleep(1)

result = subprocess.run(['xdotool', 'getwindowgeometry', window_id], 
                       capture_output=True, text=True)
print(f"\nGeometry after wmctrl:\n{result.stdout}")
