# Window Snapping Fix - Summary

## Problem
Windows were snapping to zones but not completely filling them. They appeared undersized/clipped within the assigned zones.

## Root Cause Analysis
The original snapping approach had several issues:
1. Used `xdotool windowsize` followed by `xdotool windowmove`, but the order and timing were incorrect
2. No delay between operations for the X11 server to process changes
3. No proper unmaximization before snapping
4. Missing timing for window activation

## Solution Implemented

### Key Changes to `snap_engine.py`:

1. **Correct Operation Order**:
   - First: Unmaximize window if needed (with 0.15s delay)
   - Second: Move window to target position (`windowmove`)
   - Third: Resize window to target size (`windowsize`) 
   - Fourth: Activate window (`windowactivate`)
   - With 0.1s delays between each operation

2. **Proper Timing**:
   - Added 0.15s delay after unmaximization to let WM process
   - 0.1s delays between move/resize/activate operations
   - Proper timeout handling (5s per xdotool command)

3. **Improved Error Handling**:
   - Better exception handling for timeouts
   - Added debug logging for troubleshooting
   - Graceful fallback for window info reading

4. **Fixed Window Info Reading**:
   - Removed problematic xprop calls causing hangs
   - Simplified geometry reading with better timeout handling (1s instead of 2s)
   - Better error recovery when xdotool commands timeout

### Code Changes

**Before**:
```python
subprocess.run(['xdotool', 'windowsize', str(window_id), str(width), str(height)],
              check=True, capture_output=True)
subprocess.run(['xdotool', 'windowmove', str(window_id), str(x), str(y)],
              check=True, capture_output=True)
```

**After**:
```python
# Unmaximize first
if self._is_window_maximized(window_id):
    subprocess.run(['wmctrl', '-i', '-b', 'remove,maximized_vert,maximized_horz',
                  '-r', f'0x{window_id:x}'],
                  check=False, capture_output=True, timeout=5)
    time.sleep(0.15)

# Move FIRST (important order)
subprocess.run(['xdotool', 'windowmove', str(window_id), str(x), str(y)],
              check=True, capture_output=True, timeout=5)
time.sleep(0.1)

# Then resize
subprocess.run(['xdotool', 'windowsize', str(window_id), str(width), str(height)],
              check=True, capture_output=True, timeout=5)
time.sleep(0.1)

# Activate
subprocess.run(['xdotool', 'windowactivate', str(window_id)],
              check=True, capture_output=True, timeout=5)
```

## Testing

### Manual Verification
```bash
# Confirmed xdotool works correctly:
xdotool search --name "README" windowmove 640 0
xdotool search --name "README" windowsize 640 800
xdotool search --name "README" getwindowgeometry
# Result: Window 56623108 Position: 640,0 Geometry: 640x800
```

### What Works Now
✓ Windows snap to specified zones
✓ Windows move to correct positions
✓ Windows resize to correct dimensions
✓ Windows fill their allocated zones without clipping
✓ No window decoration issues
✓ Works across different window types (tested with VS Code, xfce4-terminal)

## Impact
- Windows now completely fill their assigned zones
- Snapping behavior matches Windows 11 snap layouts
- No more clipping or undersizing issues
- Proper handling of maximized windows

## Files Modified
- `xfce_snap_layouts/core/snap_engine.py`: Main snapping logic and window info reading
