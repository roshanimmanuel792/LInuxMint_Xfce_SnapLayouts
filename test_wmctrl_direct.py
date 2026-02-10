#!/usr/bin/env python3
"""Simple test: directly call wmctrl to snap a window."""

import subprocess
import time

# Open terminal
print("Opening terminal...")
term = subprocess.Popen(['xfce4-terminal'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(2)

# Get list of windows
print("\nGetting window list...")
result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True)
print("All windows:")
print(result.stdout)

# Get the terminal window ID (should be the most recently created)
lines = result.stdout.strip().split('\n')
term_window = None
for line in lines:
    if 'Terminal' in line and 'xfce4' not in line.lower():
        parts = line.split()
        if parts:
            term_window = parts[0]
            break

if not term_window:
    # Try the last xfce4-terminal
    for line in reversed(lines):
        if 'Terminal' in line:
            parts = line.split()
            if parts:
                term_window = parts[0]
                break

if term_window:
    print(f"\nFound terminal: {term_window}")
    
    # Get current geometry
    print("\nCurrent terminal geometry:")
    result = subprocess.run(['wmctrl', '-l', '-p'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if term_window in line:
            print(f"  {line}")
    
    # Snap to left half
    print("\nSnapping to LEFT half (640x800+0+0)...")
    result = subprocess.run(['wmctrl', '-r', term_window, '-e', '0,0,0,640,800'],
                           capture_output=True, text=True)
    print(f"  Command result: {result.returncode}")
    
    time.sleep(1)
    
    # Check geometry
    print("\nGeometry after snap:")
    result = subprocess.run(['wmctrl', '-l', '-p'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if term_window in line:
            print(f"  {line}")
    
    time.sleep(2)
    
    # Snap to right half
    print("\nSnapping to RIGHT half (640x800+640+0)...")
    result = subprocess.run(['wmctrl', '-r', term_window, '-e', '0,640,0,640,800'],
                           capture_output=True, text=True)
    print(f"  Command result: {result.returncode}")
    
    time.sleep(1)
    
    # Check geometry
    print("\nGeometry after snap:")
    result = subprocess.run(['wmctrl', '-l', '-p'], capture_output=True, text=True)
    for line in result.stdout.split('\n'):
        if term_window in line:
            print(f"  {line}")
    
    time.sleep(2)
    term.terminate()
    print("\nDone!")
else:
    print("Could not find terminal window")
    term.terminate()
