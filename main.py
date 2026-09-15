import socket
import psutil
import time
from datetime import datetime


REFRESH_INTERVAL = 2


def get_service(port, protocol):
    """Find the standard service associated with a port."""

    try:
        return socket.getservbyport(port, protocol.lower())
    except OSError:
        return "Unknown"


def get_open_ports():
    """Collect all listening TCP and UDP ports."""

    ports = []

    connections = psutil.net_connections(kind="inet")

    for connection in connections:

        if connection.status != psutil.CONN_LISTEN:
            continue

        if not connection.laddr:
            continue

        # Identify protocol
        if connection.type == socket.SOCK_STREAM:
            protocol = "TCP"

        elif connection.type == socket.SOCK_DGRAM:
            protocol = "UDP"

        else:
            continue

        ip_address = connection.laddr.ip
        port_number = connection.laddr.port

        service = get_service(port_number, protocol)

        pid = connection.pid
        process_name = "N/A"

        if pid is not None:

            try:
                process = psutil.Process(pid)
                process_name = process.name()

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_name = "Unknown"

        ports.append({
            "port": port_number,
            "protocol": protocol,
            "state": connection.status,
            "service": service,
            "pid": pid if pid is not None else "N/A",
            "process": process_name,
            "address": ip_address
        })

    ports.sort(key=lambda x: (x["port"], x["protocol"]))

    return ports


def display_ports(ports):
    """Display listening ports in a table."""

    print("=" * 105)
    print("                         LINUX PORT MONITOR")
    print("=" * 105)

    print()

    print(
        f"{'PORT':<10}"
        f"{'PROTOCOL':<12}"
        f"{'STATE':<12}"
        f"{'SERVICE':<15}"
        f"{'PID':<10}"
        f"{'PROCESS':<18}"
        f"{'ADDRESS'}"
    )

    print("-" * 105)

    if not ports:

        print("No listening ports found.")

    else:

        for port in ports:

            print(
                f"{port['port']:<10}"
                f"{port['protocol']:<12}"
                f"{port['state']:<12}"
                f"{port['service']:<15}"
                f"{str(port['pid']):<10}"
                f"{port['process']:<18}"
                f"{port['address']}"
            )

    print()
    print("-" * 105)

    print(f"Total listening ports: {len(ports)}")

    print("=" * 105)


def create_port_key(port):
    """Create a unique identifier for a port."""

    return (
        port["address"],
        port["port"],
        port["protocol"]
    )


def monitor_ports():

    print()
    print("=" * 60)
    print("                 LINUX PORT MONITOR")
    print("=" * 60)

    print()
    print(f"Refresh interval: {REFRESH_INTERVAL} seconds")
    print("Monitoring started...")
    print("Press Ctrl+C to stop.")
    print()

    previous_ports = get_open_ports()

    display_ports(previous_ports)

    previous_keys = {
        create_port_key(port)
        for port in previous_ports
    }

    while True:

        time.sleep(REFRESH_INTERVAL)

        current_ports = get_open_ports()

        current_keys = {
            create_port_key(port)
            for port in current_ports
        }

        # Detect newly opened ports
        new_ports = current_keys - previous_keys

        # Detect closed ports
        closed_ports = previous_keys - current_keys

        for key in new_ports:

            address, port, protocol = key

            current_port = next(
                p for p in current_ports
                if create_port_key(p) == key
            )

            timestamp = datetime.now().strftime("%H:%M:%S")

            print(
                f"\n[+] NEW PORT DETECTED [{timestamp}]"
            )

            print(
                f"    Address : {address}"
            )

            print(
                f"    Port    : {port}"
            )

            print(
                f"    Protocol: {protocol}"
            )

            print(
                f"    Service : {current_port['service']}"
            )

            print(
                f"    PID     : {current_port['pid']}"
            )

            print(
                f"    Process : {current_port['process']}"
            )

        for key in closed_ports:

            address, port, protocol = key

            timestamp = datetime.now().strftime("%H:%M:%S")

            print(
                f"\n[-] PORT CLOSED [{timestamp}]"
            )

            print(
                f"    Address : {address}"
            )

            print(
                f"    Port    : {port}"
            )

            print(
                f"    Protocol: {protocol}"
            )

        previous_keys = current_keys


def main():

    try:
        monitor_ports()

    except KeyboardInterrupt:

        print("\n")
        print("=" * 60)
        print("Monitoring stopped.")
        print("=" * 60)


if __name__ == "__main__":
    main()
