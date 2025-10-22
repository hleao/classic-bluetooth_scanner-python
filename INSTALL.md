# Installation Guide

## Platform-Specific Installation

The installation process varies significantly by platform due to Bluetooth API differences.

### macOS (Limited Classic Bluetooth Support)

**Important**: macOS has deprecated classic Bluetooth APIs in recent versions. PyBluez does not work reliably on modern macOS (10.15+).

**Option 1: Use Bleak (Recommended for macOS)**

Bleak works with BLE devices but not classic Bluetooth SDP:

```bash
pip3 install -r requirements-bleak.txt
python3 bluetooth_scanner_bleak.py
```

**Option 2: Try PyBluez2 (May Not Work)**

```bash
pip3 install pybluez2
python3 bluetooth_scanner.py
```

If you get errors, PyBluez2 is likely incompatible with your macOS version.

**Option 3: Use Docker with Linux**

```bash
docker run -it --privileged --net=host ubuntu:22.04 bash
# Inside container:
apt update && apt install -y python3 python3-pip bluetooth libbluetooth-dev
pip3 install pybluez2
# Copy your script and run it
```

---

### Linux (Full Classic Bluetooth Support)

Linux has the best support for classic Bluetooth and SDP scanning.

**Ubuntu/Debian:**

```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip bluetooth libbluetooth-dev

# Install Python package
pip3 install -r requirements-linux.txt

# Run the scanner
python3 bluetooth_scanner.py
```

**Fedora/RHEL:**

```bash
sudo dnf install -y python3 python3-pip bluez bluez-libs-devel
pip3 install -r requirements-linux.txt
python3 bluetooth_scanner.py
```

**Arch Linux:**

```bash
sudo pacman -S python python-pip bluez bluez-utils
pip3 install -r requirements-linux.txt
python3 bluetooth_scanner.py
```

**User Permissions:**

Add your user to the `bluetooth` group:

```bash
sudo usermod -a -G bluetooth $USER
# Log out and log back in
```

---

### Windows (Experimental)

Windows support is experimental and may require additional setup.

**Requirements:**
- Windows 10 or later
- Microsoft Visual C++ Build Tools

**Installation:**

```bash
# Install Visual C++ Build Tools first from:
# https://visualstudio.microsoft.com/visual-cpp-build-tools/

pip install pybluez2
python bluetooth_scanner.py
```

---

## Testing Your Installation

### Test PyBluez Installation

```python
python3 -c "import bluetooth; print('PyBluez is working!')"
```

### Test Bleak Installation

```python
python3 -c "import bleak; print('Bleak is working!')"
```

---

## Troubleshooting

### PyBluez Installation Fails

**Error: `use_2to3 is invalid`**

This error occurs with Python 3.10+ and old PyBluez versions. Solutions:

1. Use `pybluez2` instead: `pip3 install pybluez2`
2. Use a Linux system with proper Bluetooth support
3. Use the Bleak version for BLE devices only

**Error: `bluetooth/bluetooth.h: No such file or directory`**

Install Bluetooth development libraries:
- Ubuntu/Debian: `sudo apt-get install libbluetooth-dev`
- Fedora: `sudo dnf install bluez-libs-devel`
- Arch: `sudo pacman -S bluez-libs`

### Permission Denied Errors

```bash
# Add user to bluetooth group
sudo usermod -a -G bluetooth $USER

# Or run with sudo (not recommended)
sudo python3 bluetooth_scanner.py
```

### No Devices Found

1. Ensure Bluetooth is enabled: `sudo systemctl status bluetooth`
2. Check your adapter: `hciconfig` or `bluetoothctl`
3. Make sure target devices are in discoverable mode
4. Try increasing scan duration in the script

### macOS: "Operation not permitted"

macOS requires apps to request Bluetooth permission. You may need to:
1. Grant Terminal or your IDE Bluetooth permissions in System Preferences
2. Use the Bleak version instead

---

## Recommended Setup by Use Case

| Use Case | Platform | Tool | Command |
|----------|----------|------|---------|
| Classic Bluetooth SDP scanning | Linux | PyBluez2 | `python3 bluetooth_scanner.py` |
| BLE device inspection | macOS/Linux/Windows | Bleak | `python3 bluetooth_scanner_bleak.py` |
| Development/Testing | Docker on any OS | PyBluez2 in container | See Docker option above |

---

## Alternative: Use Python 3.9 with PyBluez

If you need classic Bluetooth on macOS and nothing else works:

```bash
# Install Python 3.9 via pyenv
brew install pyenv
pyenv install 3.9.18
pyenv local 3.9.18

# Install PyBluez (NOT pybluez2)
pip install pybluez==0.23

python bluetooth_scanner.py
```

This may work on older macOS versions (10.14 or earlier).
