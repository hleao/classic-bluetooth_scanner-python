#!/usr/bin/env python3
"""
Quick test script to verify Bluetooth scanning works on your Mac
"""

import asyncio
from bleak import BleakScanner

async def quick_scan():
    print("Starting a quick 5-second Bluetooth scan...")
    print("Make sure you have granted Bluetooth permissions to your Terminal app!")
    print()

    devices = await BleakScanner.discover(timeout=5.0)

    if not devices:
        print("No devices found. This could mean:")
        print("  1. No Bluetooth devices are nearby")
        print("  2. Terminal doesn't have Bluetooth permission")
        print("     Go to: System Settings > Privacy & Security > Bluetooth")
        print("     And enable access for your Terminal app")
        return

    print(f"Found {len(devices)} device(s):\n")

    for i, device in enumerate(devices, 1):
        name = device.name if device.name else "<Unknown>"
        print(f"{i}. {name} ({device.address})")

    print("\nSuccess! Bleak is working correctly on your Mac.")
    print("You can now use: python3 bluetooth_scanner_bleak.py")

if __name__ == "__main__":
    asyncio.run(quick_scan())
