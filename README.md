# Bluetooth SDP Scanner

A Python utility for discovering Bluetooth devices and listing their services.

## Important: Platform Support

⚠️ **Classic Bluetooth SDP scanning works best on Linux**. macOS has deprecated classic Bluetooth APIs, and Windows support is experimental.

**Quick Start by Platform:**
- **Linux**: Full classic Bluetooth + SDP support → Use `bluetooth_scanner.py`
- **macOS**: BLE only (no classic Bluetooth SDP) → Use `bluetooth_scanner_bleak.py`
- **Windows**: Experimental → Use `bluetooth_scanner.py`

See [INSTALL.md](INSTALL.md) for detailed installation instructions.

## Features

### Classic Bluetooth Scanner (Linux/Windows)
- Discover nearby classic Bluetooth devices
- Interactive device selection prompt
- Complete SDP service enumeration
- Detailed service information including:
  - Service names and descriptions
  - Service UUIDs
  - Protocol information (RFCOMM channel, L2CAP PSM)
  - Service classes and profiles
  - Human-readable protocol names

### BLE Scanner (macOS/Linux/Windows)
- Discover BLE devices with signal strength (RSSI)
- Interactive device selection
- GATT service enumeration
- Characteristic inspection

## Requirements

- Python 3.9+
- Bluetooth adapter (built-in or USB)

## Quick Installation

### For Linux (Classic Bluetooth + SDP)

```bash
# Install system dependencies
sudo apt-get install bluetooth libbluetooth-dev

# Install Python package
pip3 install -r requirements-linux.txt

# Run the scanner
python3 bluetooth_scanner.py
```

### For macOS (BLE Only)

```bash
# Install Python package
pip3 install -r requirements-bleak.txt

# Run the BLE scanner
python3 bluetooth_scanner_bleak.py
```

### For Windows (Experimental)

```bash
# Install Visual C++ Build Tools first
# Then install PyBluez
pip3 install pybluez2

# Run the scanner
python3 bluetooth_scanner.py
```

**For detailed installation instructions and troubleshooting, see [INSTALL.md](INSTALL.md)**

## Usage

### Basic Usage

```bash
python bluetooth_scanner.py
```

### Make it Executable (Linux/macOS)

```bash
chmod +x bluetooth_scanner.py
./bluetooth_scanner.py
```

## Example Output

```
============================================================
  Bluetooth Device Scanner & SDP Service Lister
============================================================

[*] Scanning for Bluetooth devices (duration: 8s)...
[*] Please wait...

[+] Found 3 device(s):

#    Name                           Address
------------------------------------------------------------
1    John's iPhone                  XX:XX:XX:XX:XX:XX
2    Bluetooth Speaker              XX:XX:XX:XX:XX:XX
3    <Unknown>                      XX:XX:XX:XX:XX:XX

[?] Enter device number to connect (or 'q' to quit): 1

[+] Selected: John's iPhone (XX:XX:XX:XX:XX:XX)

[*] Querying SDP services on 'John's iPhone' (XX:XX:XX:XX:XX:XX)...
[*] This may take a moment...

[+] Found 12 service(s):

================================================================================

Service #1
--------------------------------------------------------------------------------
  Name:        Serial Port Profile (SPP)
  Service ID:  xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
  Classes:     Serial Port Profile (SPP)
  Protocols:   L2CAP, RFCOMM, Channel=1
  Port:        1

Service #2
--------------------------------------------------------------------------------
  Name:        OBEX Object Push
  Classes:     OBEX Object Push
  Protocols:   L2CAP, RFCOMM, OBEX, Channel=2
  Port:        2
...
```

## How It Works

1. **Device Discovery**: Scans for nearby Bluetooth devices using inquiry scan
2. **Interactive Selection**: Displays found devices and prompts for selection
3. **SDP Query**: Connects to selected device and queries all available SDP services
4. **Service Parsing**: Extracts and displays detailed information about each service

## Common Service Classes

The tool recognizes and displays human-readable names for common Bluetooth services:

- Serial Port Profile (SPP) - 0x1101
- OBEX Object Push - 0x1105
- Audio Source/Sink - 0x110a/0x110b
- Handsfree Profile - 0x111e
- Human Interface Device (HID) - 0x1124
- Phonebook Access (PBAP) - 0x112f
- And many more...

## Troubleshooting

### No Devices Found

- Ensure Bluetooth is enabled on your computer
- Make sure target devices are in discoverable/pairing mode
- Check that devices are within range (typically 10-30 feet)
- On Linux, ensure your user has permission to access Bluetooth

### Permission Errors (Linux)

```bash
sudo usermod -a -G bluetooth $USER
# Log out and back in
```

### PyBluez Installation Issues

If you encounter issues installing PyBluez, consult the [PyBluez documentation](https://github.com/pybluez/pybluez).

## Security Note

This tool performs passive scanning and service discovery only. It does not attempt to pair with or authenticate to devices. Some devices may not respond to SDP queries from unpaired devices.

## License

MIT License - Feel free to use and modify as needed.
