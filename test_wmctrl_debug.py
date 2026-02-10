#!/usr/bin/env python3
"""Debug wmctrl snapping."""

import subprocess
import time

# Open terminal and get its window ID
print("Opening terminal...")
term_proc = subprocess.Popen(['xfce4-terminal'])
time.sleep(3)

# List all windows
print("\nWindows:")
result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
print(result.stdout)

# Find terminal window (not xfce4-panel)
term_id = None
for line in result.stdout.split('\n'):
    if 'Terminal' in line and '0x' in line:
        parts = line.split()
        if parts and len(parts) > 0:
            term_id = parts[0]
            if 'xfce4-panel' not in line:
                print(f"\nUsing terminal: {term_id}")
                break

if term_id:
    # Get current geometry
    print("\nCurrent geometry of terminal:")
    result = subprocess.run(['wmctrl', '-l', '-p'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if term_id in line:
            print(f"  {line}")
    
    # Construct wmctrl command
    cmd = ['wmctrl', '-r', term_id, '-b', 'remove,maximized_vert,maximized_horz',
           '-e', '0,0,0,640,800']
    
    print(f"\nExecuting: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(f"Return code: {result.returncode}")
    if result.stderr:
        print(f"Stderr: {result.stderr}")
    
    time.sleep(1)
    
    # Check new geometry
    print("\nGeometry after snap:")
    result = subprocess.run(['wmctrl', '-l', '-p'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if term_id in line:
            print(f"  {line}")
            # Parse and check
            parts = line.split()
            if len(parts) >= 6:
                x, y, w, h = int(parts[2]), int(parts[3]), int(parts[4]), int(parts[5])
                print(f"  Parsed: {w}x{h}+{x}+{y}")
                if w == 640 and h == 800 and x == 0 and y == 0:
                    print("  ✓ SUCCESS: Window snapped correctly!")
                else:
                    print("  ✗ FAILED: Window did not snap correctly")
    
    time.sleep(2)
    term_proc.terminate()
else:
    print("\nCould not find terminal window ID")
    term_proc.terminate()
