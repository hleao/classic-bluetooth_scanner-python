#!/usr/bin/env python3
"""
Bluetooth Device Scanner and SDP Service Lister (Bleak version)

This utility allows you to:
1. Discover nearby Bluetooth devices (classic and BLE)
2. Interactively select a device to connect to
3. Attempt to list SDP services (limited on modern macOS)

Requirements:
    - bleak: pip install bleak

Note: macOS has limited classic Bluetooth support. This version focuses on
device discovery. For full SDP support, Linux is recommended.
"""

import asyncio
import sys
from typing import List, Optional, Tuple
from bleak import BleakScanner


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("  Bluetooth Device Scanner (Bleak version)")
    print("=" * 60)
    print()
    print("[!] Note: macOS has limited classic Bluetooth support.")
    print("[!] This scanner will show BLE devices.")
    print("[!] For full SDP scanning, use Linux with PyBluez.\n")


async def discover_devices(duration: int = 8) -> List[Tuple[str, str, int]]:
    """
    Discover nearby Bluetooth devices using Bleak.

    Args:
        duration: Duration of the scan in seconds (default: 8)

    Returns:
        List of tuples containing (address, name, rssi) for each device found
    """
    print(f"[*] Scanning for Bluetooth devices (duration: {duration}s)...")
    print("[*] Please wait...\n")

    try:
        devices = await BleakScanner.discover(timeout=duration, return_adv=True)

        device_list = []
        for addr, (device, adv_data) in devices.items():
            name = device.name if device.name else "<Unknown>"
            rssi = adv_data.rssi if hasattr(adv_data, 'rssi') else 0
            device_list.append((device.address, name, rssi))

        # Sort by RSSI (signal strength) descending
        device_list.sort(key=lambda x: x[2], reverse=True)
        return device_list

    except Exception as e:
        print(f"[!] Error during device discovery: {e}")
        return []


def display_devices(devices: List[Tuple[str, str, int]]) -> None:
    """
    Display discovered devices in a formatted table.

    Args:
        devices: List of (address, name, rssi) tuples
    """
    if not devices:
        print("[!] No devices found.")
        return

    print(f"[+] Found {len(devices)} device(s):\n")
    print(f"{'#':<4} {'Name':<30} {'Address':<20} {'RSSI':<6}")
    print("-" * 65)

    for idx, (addr, name, rssi) in enumerate(devices, 1):
        rssi_str = f"{rssi} dBm" if rssi != 0 else "N/A"
        print(f"{idx:<4} {name:<30} {addr:<20} {rssi_str:<6}")
    print()


def select_device(devices: List[Tuple[str, str, int]]) -> Optional[Tuple[str, str, int]]:
    """
    Interactive prompt for device selection.

    Args:
        devices: List of (address, name, rssi) tuples

    Returns:
        Selected device tuple (address, name, rssi) or None if cancelled
    """
    while True:
        try:
            choice = input("[?] Enter device number to inspect (or 'q' to quit): ").strip()

            if choice.lower() == 'q':
                return None

            device_num = int(choice)

            if 1 <= device_num <= len(devices):
                return devices[device_num - 1]
            else:
                print(f"[!] Please enter a number between 1 and {len(devices)}")
        except ValueError:
            print("[!] Invalid input. Please enter a number or 'q' to quit.")
        except KeyboardInterrupt:
            print("\n[!] Cancelled by user.")
            return None


async def inspect_device(device_address: str, device_name: str) -> None:
    """
    Inspect a BLE device and show available information.

    Args:
        device_address: Bluetooth address of the device
        device_name: Name of the device
    """
    print(f"\n[*] Inspecting device '{device_name}' ({device_address})...")
    print("[*] This may take a moment...\n")

    try:
        from bleak import BleakClient

        async with BleakClient(device_address, timeout=15.0) as client:
            print(f"[+] Connected to {device_name}\n")
            print("=" * 80)

            # Get all services
            services = client.services

            if not services:
                print("[!] No GATT services found on this device.")
                return

            print(f"[+] Found {len(services)} GATT service(s):\n")

            for idx, service in enumerate(services, 1):
                print(f"\nService #{idx}")
                print("-" * 80)
                print(f"  UUID:        {service.uuid}")
                print(f"  Handle:      {service.handle}")
                print(f"  Description: {service.description}")

                # List characteristics
                if service.characteristics:
                    print(f"  Characteristics ({len(service.characteristics)}):")
                    for char in service.characteristics:
                        print(f"    - UUID: {char.uuid}")
                        print(f"      Handle: {char.handle}")
                        print(f"      Properties: {', '.join(char.properties)}")
                        if char.description:
                            print(f"      Description: {char.description}")
                        print()

            print("=" * 80)
            print(f"[+] Total services listed: {len(services)}\n")

    except asyncio.TimeoutError:
        print("[!] Connection timeout. Device may not support connections or is out of range.")
    except Exception as e:
        print(f"[!] Error while inspecting device: {e}")
        print("[!] Note: Some devices don't allow connections from unpaired clients.")


async def main():
    """Main application flow"""
    print_banner()

    # Step 1: Discover devices
    devices = await discover_devices()

    if not devices:
        print("[!] No devices found. Please ensure:")
        print("    - Bluetooth is enabled on this computer")
        print("    - Target devices are powered on and in range")
        sys.exit(1)

    # Step 2: Display devices
    display_devices(devices)

    # Step 3: Interactive device selection
    selected_device = select_device(devices)

    if not selected_device:
        print("[*] Exiting...")
        sys.exit(0)

    device_address, device_name, rssi = selected_device

    print(f"\n[+] Selected: {device_name} ({device_address})")

    # Step 4: Inspect device
    await inspect_device(device_address, device_name)

    print("[*] Scan complete!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        sys.exit(1)
