#!/usr/bin/env python3
import socket
import subprocess
import platform
import re
import struct

A_DOIP_CTRL = 2  # 2s timeout
UDP_DISCOVERY = 13400  # port number
UDP_BROADCAST = "255.255.255.255"

DOIP_MSG_TYPE_VEHICLE_IDENTIFICATION_REQUEST = 0x0001
DOIP_MSG_TYPE_VEHICLE_IDENTIFICATION_RESPONSE = 0x0004


def _add_header(type, payload=b""):
    header = struct.pack(
        "!BBHL",
        0x2,
        0xFF ^ 0x2,
        type,
        len(payload),
    )
    header += payload

    return header


def _strip_header(packet):
    header = struct.unpack("!BBHL", packet[:8])
    protocol_version = header[0]
    inverse_protocol_version = header[1]
    payload_type = header[2]
    payload_length = header[3]

    payload = packet[8:]

    if protocol_version ^ 0xFF != inverse_protocol_version:
        return None, None

    return payload_type, payload


def _parse_vehicle_identification_response(payload):
    unpack_fmt_str = "!17sH6s6sB"
    if len(payload) == 33:
        unpack_fmt_str += "B"
    data = struct.unpack(unpack_fmt_str, payload)
    vin = data[0].decode().strip()
    return vin


def _extract_windows_interface_data():
    if_list = []

    def _get_or_create_if_data(if_name):
        for if_data in if_list:
            if if_data["name"] == if_name:
                return if_data

        new_if_data = {"name": if_name, "ips": [], "subnets": []}
        if_list.append(new_if_data)
        return new_if_data

    re_if_data = re.compile(r"^(.+)(?<!\s)\s+([\d\.]+)\s+(\d+)$")
    res = subprocess.run(
        [
            "powershell",
            "-Command",
            (
                "Get-NetIPInterface | "
                "Where-Object {$_.ConnectionState -eq 'Connected' -and $_.AddressFamily -eq 'IPv4'} | "
                "Get-NetIPAddress | "
                "Select-Object InterfaceAlias, IPAddress, PrefixLength"
            ),
        ],
        text=True,
        capture_output=True,
    )
    if res.returncode == 0:
        lines = res.stdout.splitlines()
        for l in lines:
            if (m := re_if_data.match(l)) is not None:
                if_data = _get_or_create_if_data(m.group(1))
                if_data["ips"].append(m.group(2))
                if_data["subnets"].append(m.group(3))

        return if_list
    else:
        raise RuntimeError("Unable to retrieve interface data")


def all_interfaces():
    if platform.system() == "Windows":
        return _extract_windows_interface_data()
    else:
        assert "Only Windows supported for now"


def main():
    if_list = all_interfaces()
    vehicle_found = False
    result = []

    for if_data in if_list:
        for ip in if_data["ips"]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            sock.settimeout(A_DOIP_CTRL)

            msg = _add_header(DOIP_MSG_TYPE_VEHICLE_IDENTIFICATION_REQUEST)
            sock.bind((ip, 0))
            sock.sendto(msg, (UDP_BROADCAST, UDP_DISCOVERY))

            try:
                data, addr = sock.recvfrom(1024)
                type, payload = _strip_header(data)

                if type == DOIP_MSG_TYPE_VEHICLE_IDENTIFICATION_RESPONSE:
                    vin = _parse_vehicle_identification_response(payload)
                    result.append(f"IP: {addr[0]}\nVIN: {vin}\n")
                    vehicle_found = True

            except socket.timeout:
                pass

            sock.close()

    if not vehicle_found:
        result.append("No vehicle is connected to PC")

    return '\n'.join(result)


if __name__ == "__main__":
    print(main())
