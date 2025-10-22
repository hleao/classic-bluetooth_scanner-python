#!/usr/bin/env python3
"""
Bluetooth Device Scanner and SDP Service Lister

This utility allows you to:
1. Discover nearby classic Bluetooth devices
2. Interactively select a device to connect to
3. List all SDP (Service Discovery Protocol) services available on the device

Requirements:
    - PyBluez: pip install pybluez
"""

import bluetooth
import sys
from typing import List, Dict, Optional, Tuple


def print_banner():
    """Print application banner"""
    print("=" * 60)
    print("  Bluetooth Device Scanner & SDP Service Lister")
    print("=" * 60)
    print()


def discover_devices(duration: int = 8) -> List[Tuple[str, str]]:
    """
    Discover nearby Bluetooth devices.

    Args:
        duration: Duration of the scan in seconds (default: 8)

    Returns:
        List of tuples containing (address, name) for each device found
    """
    print(f"[*] Scanning for Bluetooth devices (duration: {duration}s)...")
    print("[*] Please wait...\n")

    try:
        nearby_devices = bluetooth.discover_devices(
            duration=duration,
            lookup_names=True,
            flush_cache=True,
            lookup_class=False
        )
        return nearby_devices
    except Exception as e:
        print(f"[!] Error during device discovery: {e}")
        return []


def display_devices(devices: List[Tuple[str, str]]) -> None:
    """
    Display discovered devices in a formatted table.

    Args:
        devices: List of (address, name) tuples
    """
    if not devices:
        print("[!] No devices found.")
        return

    print(f"[+] Found {len(devices)} device(s):\n")
    print(f"{'#':<4} {'Name':<30} {'Address':<20}")
    print("-" * 60)

    for idx, (addr, name) in enumerate(devices, 1):
        device_name = name if name else "<Unknown>"
        print(f"{idx:<4} {device_name:<30} {addr:<20}")
    print()


def select_device(devices: List[Tuple[str, str]]) -> Optional[Tuple[str, str]]:
    """
    Interactive prompt for device selection.

    Args:
        devices: List of (address, name) tuples

    Returns:
        Selected device tuple (address, name) or None if cancelled
    """
    while True:
        try:
            choice = input("[?] Enter device number to connect (or 'q' to quit): ").strip()

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


def parse_protocol_descriptor(proto_desc_list) -> Dict[str, any]:
    """
    Parse protocol descriptor list to extract protocol information.

    Args:
        proto_desc_list: Protocol descriptor list from SDP record

    Returns:
        Dictionary with protocol information
    """
    protocols = {}

    try:
        for proto_desc in proto_desc_list:
            if isinstance(proto_desc, (list, tuple)) and len(proto_desc) > 0:
                proto_uuid = proto_desc[0]

                # Map common protocol UUIDs to names
                if proto_uuid == bluetooth.L2CAP_UUID:
                    protocols['L2CAP'] = True
                    if len(proto_desc) > 1:
                        protocols['PSM'] = proto_desc[1]
                elif proto_uuid == bluetooth.RFCOMM_UUID:
                    protocols['RFCOMM'] = True
                    if len(proto_desc) > 1:
                        protocols['Channel'] = proto_desc[1]
                elif proto_uuid == bluetooth.OBEX_UUID:
                    protocols['OBEX'] = True
                elif proto_uuid == bluetooth.TCP_UUID:
                    protocols['TCP'] = True
                elif proto_uuid == bluetooth.UDP_UUID:
                    protocols['UDP'] = True
    except Exception as e:
        protocols['parse_error'] = str(e)

    return protocols


def get_service_class_name(uuid: str) -> str:
    """
    Get human-readable name for common service class UUIDs.

    Args:
        uuid: Service class UUID

    Returns:
        Human-readable service name
    """
    # Common Bluetooth service class UUIDs
    service_classes = {
        "0x1101": "Serial Port Profile (SPP)",
        "0x1105": "OBEX Object Push",
        "0x1106": "OBEX File Transfer",
        "0x110a": "Audio Source",
        "0x110b": "Audio Sink",
        "0x110c": "A/V Remote Control Target",
        "0x110e": "A/V Remote Control",
        "0x110f": "Video Conferencing",
        "0x1112": "Headset - Audio Gateway (AG)",
        "0x1115": "Personal Area Network (PANU)",
        "0x1116": "Network Access Point (NAP)",
        "0x1117": "Group Network (GN)",
        "0x111e": "Handsfree",
        "0x111f": "Handsfree Audio Gateway",
        "0x1124": "Human Interface Device (HID)",
        "0x1126": "HID Keyboard",
        "0x1127": "HID Mouse",
        "0x112d": "SIM Access",
        "0x112f": "Phonebook Access (PBAP)",
        "0x1130": "Phonebook Access PSE",
        "0x1132": "Message Access Server",
        "0x1203": "Generic Audio",
    }

    uuid_str = uuid if isinstance(uuid, str) else hex(uuid) if isinstance(uuid, int) else str(uuid)
    return service_classes.get(uuid_str, uuid_str)


def list_sdp_services(device_address: str, device_name: str) -> None:
    """
    List all SDP services available on the specified device.

    Args:
        device_address: Bluetooth MAC address of the device
        device_name: Name of the device
    """
    print(f"\n[*] Querying SDP services on '{device_name}' ({device_address})...")
    print("[*] This may take a moment...\n")

    try:
        services = bluetooth.find_service(address=device_address)

        if not services:
            print("[!] No SDP services found on this device.")
            return

        print(f"[+] Found {len(services)} service(s):\n")
        print("=" * 80)

        for idx, service in enumerate(services, 1):
            print(f"\nService #{idx}")
            print("-" * 80)

            # Service Name
            name = service.get("name", "<Unnamed Service>")
            print(f"  Name:        {name}")

            # Service Description
            description = service.get("description", "")
            if description:
                print(f"  Description: {description}")

            # Service Provider
            provider = service.get("provider", "")
            if provider:
                print(f"  Provider:    {provider}")

            # Service ID (UUID)
            service_id = service.get("service-id", "")
            if service_id:
                print(f"  Service ID:  {service_id}")

            # Service Classes
            service_classes = service.get("service-classes", [])
            if service_classes:
                print(f"  Classes:     ", end="")
                class_names = [get_service_class_name(str(sc)) for sc in service_classes]
                print(", ".join(class_names))

            # Profiles
            profiles = service.get("profiles", [])
            if profiles:
                print(f"  Profiles:    {profiles}")

            # Protocol Descriptors
            proto_desc = service.get("protocol")
            if proto_desc:
                protocols = parse_protocol_descriptor(proto_desc)
                if protocols:
                    print(f"  Protocols:   ", end="")
                    proto_strs = []
                    for key, value in protocols.items():
                        if isinstance(value, bool) and value:
                            proto_strs.append(key)
                        elif not isinstance(value, bool):
                            proto_strs.append(f"{key}={value}")
                    print(", ".join(proto_strs))

            # Host and Port (if available)
            host = service.get("host", "")
            port = service.get("port", "")
            if host:
                print(f"  Host:        {host}")
            if port:
                print(f"  Port:        {port}")

        print("\n" + "=" * 80)
        print(f"[+] Total services listed: {len(services)}\n")

    except bluetooth.BluetoothError as e:
        print(f"[!] Bluetooth error while querying services: {e}")
    except Exception as e:
        print(f"[!] Error while querying SDP services: {e}")


def main():
    """Main application flow"""
    print_banner()

    # Step 1: Discover devices
    devices = discover_devices()

    if not devices:
        print("[!] No devices found. Please ensure:")
        print("    - Bluetooth is enabled on this computer")
        print("    - Target devices are in pairing/discoverable mode")
        print("    - Target devices are within range")
        sys.exit(1)

    # Step 2: Display devices
    display_devices(devices)

    # Step 3: Interactive device selection
    selected_device = select_device(devices)

    if not selected_device:
        print("[*] Exiting...")
        sys.exit(0)

    device_address, device_name = selected_device
    device_name = device_name if device_name else "<Unknown>"

    print(f"\n[+] Selected: {device_name} ({device_address})")

    # Step 4: List SDP services
    list_sdp_services(device_address, device_name)

    print("[*] Scan complete!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        sys.exit(1)
