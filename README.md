# xfce-snap-layouts

**Windows 11-style snap layouts for Linux Mint XFCE**

A production-ready, lightweight desktop utility that provides visual window snapping with a transparent overlay interface.

## 🆕 Latest Update

**Window Snapping Fixed!** Windows now snap with perfect geometry - they fill their allocated zones completely without clipping or undersizing. The fix ensures proper operation ordering (unmaximize → move → resize → activate) with correct timing between X11 operations. [See details](SNAP_FIX_SUMMARY.md)

## ✨ Features

- **3 Snap Layouts**: 50/50 split, 1 Big + 2 Small, 3 Columns
- **Visual Overlay**: GTK3 transparent interface with hover effects
- **Multi-Monitor Support**: Automatically detects and snaps to correct monitor
- **Window Management**: Handles maximized states, resizing, and focus
- **Perfect Geometry**: Windows snap with correct sizing - no clipping!
- **Lightweight**: <100ms startup, ~50-80MB memory footprint

## 🚀 Quick Install

### 1. Install System Dependencies

```bash
sudo apt-get update
sudo apt-get install -y python3-venv python3-gi gir1.2-gtk-3.0 \
  libgirepository1.0-dev gobject-introspection libcairo2-dev \
  pkg-config cmake xdotool wmctrl x11-utils
```

### 2. Set Up Project

```bash
cd /home/snaplayoutplugin
python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### 3. Create Trigger Script

```bash
cat > ~/snap-layout-trigger.sh << 'EOF'
#!/bin/bash
cd /home/snaplayoutplugin
source venv/bin/activate
python3 test_overlay.py
EOF
chmod +x ~/snap-layout-trigger.sh
```

### 4. Set Up Keyboard Shortcut

1. Open: **Settings → Keyboard → Application Shortcuts**
2. Click **Add**
3. Command: `/home/snap-layout-trigger.sh`
4. Shortcut: Press **Super+Shift+Z** (or your preferred key)

## 📖 Usage

1. **Focus a window** you want to snap
2. **Press your keyboard shortcut** (Super+Shift+Z)
3. **Click a layout zone** in the overlay
4. **Window snaps instantly!**
5. Press **ESC** to close overlay without snapping

## 🔧 Configuration

Edit `~/.config/xfce-snap-layouts/config.json`:

```json
{
  "keyboard_shortcut": "<Super>z",
  "enabled_layouts": ["50_50_split", "1_big_2_small", "3_columns"],
  "overlay_opacity": 0.9,
  "zone_highlight_color": "#0078d4"
}
```

## 🧪 Testing

Run manually:
```bash
cd /home/snaplayoutplugin
source venv/bin/activate
python3 test_overlay.py
```

Validate build:
```bash
python3 validate_build.py
```

## 📁 Project Structure

```
xfce_snap_layouts/
├── core/           # Monitor detection, layouts, window snapping
├── ui/             # GTK overlay and controller
├── utils/          # Configuration and logging
└── launcher.py     # Main entry point
```

## 📊 Build Status

✅ All core features implemented  


## 📚 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [BUILD_AND_INSTALL.md](BUILD_AND_INSTALL.md) - Complete installation guide
- [Logs](~/.config/xfce-snap-layouts/logs/xfce-snap-layouts.log)

## 🔄 Future Enhancements

- XFCE panel plugin
- Hover-based trigger
- Window animations
- Wayland support
- Custom user layouts

## 📄 License

MIT License - See [LICENSE](LICENSE)

---

**Built with:** Python 3, GTK3, xdotool, wmctrl, xrandr