#!/usr/bin/env python3
"""Validation and testing script for xfce-snap-layouts."""

import sys
import subprocess
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).parent
XFCE_SNAP_LAYOUTS = PROJECT_ROOT / "xfce_snap_layouts"


def check_dependencies() -> bool:
    """Check system and Python dependencies."""
    logger.info("Checking system dependencies...")
    
    # Check system tools
    system_tools = ['xdotool', 'wmctrl', 'xrandr', 'xprop']
    missing_tools = []
    
    for tool in system_tools:
        try:
            subprocess.run(['which', tool], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            missing_tools.append(tool)
    
    if missing_tools:
        logger.error(f"Missing system tools: {', '.join(missing_tools)}")
        logger.info("Install with: sudo apt-get install xdotool wmctrl x11-utils")
        return False
    
    logger.info("✓ All system dependencies found")
    
    # Check Python dependencies
    logger.info("Checking Python dependencies...")
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk, Gdk
        logger.info("✓ PyGObject and GTK3 available")
    except ImportError as e:
        logger.error(f"Missing Python dependency: {e}")
        logger.info("Install with: pip install PyGObject")
        return False
    
    return True


def verify_imports() -> bool:
    """Verify all module imports work."""
    logger.info("Verifying module imports...")
    
    modules_to_test = [
        ('xfce_snap_layouts.utils.config', 'config_manager'),
        ('xfce_snap_layouts.utils.logger', 'setup_logging'),
        ('xfce_snap_layouts.core.monitor', 'monitor_manager'),
        ('xfce_snap_layouts.core.layout_engine', 'layout_engine'),
        ('xfce_snap_layouts.core.snap_engine', 'snap_engine'),
        ('xfce_snap_layouts.core.keyboard_hook', 'keyboard_hook_manager'),
        ('xfce_snap_layouts.ui.overlay', 'overlay_manager'),
        ('xfce_snap_layouts.ui.controller', 'controller'),
    ]
    
    for module_name, component_name in modules_to_test:
        try:
            module = __import__(module_name, fromlist=[component_name])
            getattr(module, component_name)
            logger.info(f"✓ {module_name}.{component_name}")
        except Exception as e:
            logger.error(f"✗ Failed to import {module_name}.{component_name}: {e}")
            return False
    
    return True


def test_core_modules() -> bool:
    """Test core module functionality."""
    logger.info("Testing core modules...")
    
    try:
        # Test monitor detection
        from xfce_snap_layouts.core import monitor_manager
        monitors = monitor_manager.get_all_monitors()
        logger.info(f"✓ Detected {len(monitors)} monitor(s)")
        for mon in monitors:
            logger.info(f"  - {mon.name}: {mon.width}x{mon.height}+{mon.x}+{mon.y}")
        
        # Test layout engine
        from xfce_snap_layouts.core import layout_engine
        layouts = layout_engine.get_all_layouts()
        logger.info(f"✓ Found {len(layouts)} layout(s)")
        for layout in layouts:
            logger.info(f"  - {layout.name} ({len(layout.zones)} zones)")
        
        # Test configuration
        from xfce_snap_layouts.utils import config_manager
        config = config_manager.config
        logger.info(f"✓ Configuration loaded:")
        logger.info(f"  - Hotkey: {config_manager.get('keyboard_shortcut')}")
        logger.info(f"  - Layouts: {len(config_manager.get('enabled_layouts'))} enabled")
        
        return True
    except Exception as e:
        logger.error(f"Error testing core modules: {e}")
        return False


def check_file_structure() -> bool:
    """Verify project file structure."""
    logger.info("Checking project structure...")
    
    required_files = [
        'setup.py',
        'requirements.txt',
        'LICENSE',
        'BUILD_AND_INSTALL.md',
        'Makefile',
        '.gitignore',
        'xfce_snap_layouts/__init__.py',
        'xfce_snap_layouts/launcher.py',
        'xfce_snap_layouts/core/__init__.py',
        'xfce_snap_layouts/core/monitor.py',
        'xfce_snap_layouts/core/layout_engine.py',
        'xfce_snap_layouts/core/snap_engine.py',
        'xfce_snap_layouts/core/keyboard_hook.py',
        'xfce_snap_layouts/ui/__init__.py',
        'xfce_snap_layouts/ui/overlay.py',
        'xfce_snap_layouts/ui/controller.py',
        'xfce_snap_layouts/utils/__init__.py',
        'xfce_snap_layouts/utils/config.py',
        'xfce_snap_layouts/utils/logger.py',
    ]
    
    missing_files = []
    for file_path in required_files:
        full_path = PROJECT_ROOT / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        logger.error(f"Missing files: {missing_files}")
        return False
    
    logger.info(f"✓ All {len(required_files)} required files present")
    return True


def check_python_syntax() -> bool:
    """Check all Python files for syntax errors."""
    logger.info("Checking Python syntax...")
    
    py_files = list(XFCE_SNAP_LAYOUTS.rglob('*.py'))
    
    for py_file in py_files:
        try:
            with open(py_file, 'r') as f:
                compile(f.read(), py_file, 'exec')
        except SyntaxError as e:
            logger.error(f"Syntax error in {py_file}: {e}")
            return False
    
    logger.info(f"✓ All {len(py_files)} Python files have valid syntax")
    return True


def main() -> int:
    """Run all validation checks."""
    logger.info("=" * 60)
    logger.info("xfce-snap-layouts - Build Validation")
    logger.info("=" * 60)
    
    checks = [
        ("File Structure", check_file_structure),
        ("Python Syntax", check_python_syntax),
        ("System Dependencies", check_dependencies),
        ("Module Imports", verify_imports),
        ("Core Functionality", test_core_modules),
    ]
    
    results = []
    for check_name, check_func in checks:
        logger.info("")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            logger.error(f"Unexpected error during {check_name}: {e}")
            results.append((check_name, False))
    
    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("Validation Summary")
    logger.info("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {check_name}")
    
    logger.info("")
    logger.info(f"Result: {passed}/{total} checks passed")
    
    if passed == total:
        logger.info("✓ Build validation successful!")
        return 0
    else:
        logger.error("✗ Build validation failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main())
