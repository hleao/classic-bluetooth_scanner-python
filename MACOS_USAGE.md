# macOS Usage Guide

## Setup Complete!

Bleak has been successfully installed and tested on your M1 MacBook Air.

## Quick Start

### Run the Bluetooth Scanner

```bash
python3 bluetooth_scanner_bleak.py
```

This will:
1. Scan for nearby BLE devices (8 seconds)
2. Display a list of found devices with signal strength
3. Let you select a device to inspect
4. Connect and show all GATT services and characteristics

### Test Scan

For a quick test, run:

```bash
python3 test_bluetooth.py
```

## What You Can Do

### Device Discovery
The scanner finds BLE (Bluetooth Low Energy) devices including:
- Smartphones (iPhones, Android phones)
- Bluetooth headphones and speakers
- Fitness trackers and smartwatches
- Smart home devices
- IoT sensors
- And any other BLE-enabled device

### Service Inspection
Once connected to a device, you'll see:
- **GATT Services**: The services exposed by the device
- **Service UUIDs**: Unique identifiers for each service
- **Characteristics**: Individual data points within services
- **Properties**: What operations are supported (read, write, notify, etc.)

## Example Session

```bash
$ python3 bluetooth_scanner_bleak.py

============================================================
  Bluetooth Device Scanner (Bleak version)
============================================================

[!] Note: macOS has limited classic Bluetooth support.
[!] This scanner will show BLE devices.
[!] For full SDP scanning, use Linux with PyBluez.

[*] Scanning for Bluetooth devices (duration: 8s)...
[*] Please wait...

[+] Found 4 device(s):

#    Name                           Address                                RSSI
-----------------------------------------------------------------
1    CoolStripMic                   54560F07-73EE-184B-192F-99A532BBE873   -65 dBm
2    <Unknown>                      C7287F05-8E86-8D74-6653-8E7148B41CA4   -78 dBm
3    Hugo's iPhone                  7CEDA053-9A48-B4DF-4DDB-BBB7F1C014B4   -45 dBm
4    <Unknown>                      F6318DD3-8E0D-B445-1917-C749F2767992   -82 dBm

[?] Enter device number to inspect (or 'q' to quit): 3

[+] Selected: Hugo's iPhone (7CEDA053-9A48-B4DF-4DDB-BBB7F1C014B4)

[*] Inspecting device 'Hugo's iPhone' (7CEDA053-9A48-B4DF-4DDB-BBB7F1C014B4)...
[*] This may take a moment...

[+] Connected to Hugo's iPhone

================================================================================
[+] Found 8 GATT service(s):

Service #1
--------------------------------------------------------------------------------
  UUID:        00001800-0000-1000-8000-00805f9b34fb
  Handle:      1
  Description: Generic Access Profile
  Characteristics (3):
    - UUID: 00002a00-0000-1000-8000-00805f9b34fb
      Handle: 2
      Properties: read
      Description: Device Name

    - UUID: 00002a01-0000-1000-8000-00805f9b34fb
      Handle: 4
      Properties: read
      Description: Appearance

...
```

## Important Notes

### Bluetooth Permissions

Make sure your Terminal app (or IDE) has Bluetooth permission:

1. Go to **System Settings** (or System Preferences)
2. Click **Privacy & Security**
3. Click **Bluetooth**
4. Enable access for your Terminal app (Terminal, iTerm2, VS Code, etc.)

### BLE vs Classic Bluetooth

**What this scanner does:**
- ✅ Discovers BLE (Bluetooth Low Energy) devices
- ✅ Connects to BLE devices
- ✅ Lists GATT services and characteristics
- ✅ Shows signal strength (RSSI)

**What it cannot do on macOS:**
- ❌ Classic Bluetooth discovery (pre-4.0 devices)
- ❌ SDP (Service Discovery Protocol) for classic Bluetooth
- ❌ RFCOMM connections
- ❌ Classic Bluetooth file transfers

For classic Bluetooth SDP scanning, you need Linux. See [INSTALL.md](INSTALL.md) for Linux setup.

### Common Use Cases

1. **Find Your Lost Bluetooth Device**: Use RSSI to locate devices by signal strength
2. **IoT Development**: Inspect services on your BLE sensors
3. **Security Research**: Enumerate services on BLE devices
4. **Smart Home**: Discover and inspect smart home devices
5. **Fitness Tracking**: See what data your fitness tracker exposes

## Troubleshooting

### "No devices found"

- Make sure Bluetooth is enabled on your Mac
- Check that devices are powered on and in range
- Some devices only advertise when in pairing mode
- Grant Bluetooth permissions to your Terminal app

### "Connection timeout"

- Device may be too far away
- Device may not allow connections from unpaired clients
- Try pairing the device with macOS first (System Settings > Bluetooth)

### Permission denied errors

- Go to System Settings > Privacy & Security > Bluetooth
- Enable access for your Terminal application

## Next Steps

### For Classic Bluetooth (SDP)

If you need to scan classic Bluetooth devices and enumerate SDP services:

1. Use a Linux machine or VM
2. Follow the instructions in [INSTALL.md](INSTALL.md)
3. Use `bluetooth_scanner.py` instead

### Customization

The scanner code is well-documented and easy to modify:
- Change scan duration (default: 8 seconds)
- Filter devices by RSSI threshold
- Auto-connect to specific devices by name
- Read/write characteristics (requires adding code)

## Files in This Project

- `bluetooth_scanner_bleak.py` - BLE scanner (use this on macOS)
- `bluetooth_scanner.py` - Classic Bluetooth scanner (Linux/Windows)
- `test_bluetooth.py` - Quick test script
- `requirements-bleak.txt` - Bleak dependencies
- `requirements-linux.txt` - PyBluez dependencies (Linux)
- `INSTALL.md` - Detailed installation guide
- `README.md` - Project overview

## Support

For issues with:
- **Bleak**: https://github.com/hbldh/bleak
- **BLE in general**: https://www.bluetooth.com/
- **This project**: Check [INSTALL.md](INSTALL.md) for troubleshooting

Happy Bluetooth scanning!
