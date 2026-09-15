import socket
import ipaddress
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


# ============================================================
# CONFIGURATION
# ============================================================

START_PORT = 1
END_PORT = 65535

SCAN_TIMEOUT = 0.3
MAX_WORKERS = 200
BATCH_SIZE = 2000


# ============================================================
# IP VALIDATION
# ============================================================

def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


# ============================================================
# PORT SCANNING
# ============================================================

def scan_port(target_ip, port):

    start_time = time.perf_counter()

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(SCAN_TIMEOUT)

    try:
        result = sock.connect_ex(
            (target_ip, port)
        )

        response_time = (
            time.perf_counter() - start_time
        ) * 1000

        # OPEN
        if result == 0:

            return {
                "port": port,
                "state": "OPEN",
                "response_time": response_time
            }

        # CLOSED
        elif result == 111:

            return {
                "port": port,
                "state": "CLOSED",
                "response_time": response_time
            }

        # FILTERED / NO RESPONSE
        else:

            return {
                "port": port,
                "state": "FILTERED",
                "response_time": response_time
            }

    except socket.timeout:

        response_time = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "port": port,
            "state": "FILTERED",
            "response_time": response_time
        }

    except OSError:

        response_time = (
            time.perf_counter() - start_time
        ) * 1000

        return {
            "port": port,
            "state": "FILTERED",
            "response_time": response_time
        }

    finally:

        sock.close()


# ============================================================
# SERVICE DETECTION
# ============================================================

def get_service(port):

    try:

        return socket.getservbyport(
            port,
            "tcp"
        )

    except OSError:

        return "Unknown"


# ============================================================
# BANNER / VERSION DETECTION
# ============================================================

def get_banner(target_ip, port):

    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    sock.settimeout(2.0)

    try:

        sock.connect(
            (target_ip, port)
        )

        # ----------------------------------------------------
        # Try to receive an initial banner
        # ----------------------------------------------------

        try:

            banner = sock.recv(2048)

            if banner:

                text = banner.decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if text:

                    return text

        except socket.timeout:

            pass

        # ----------------------------------------------------
        # HTTP detection
        # ----------------------------------------------------

        if port in (
            80,
            81,
            443,
            8000,
            8008,
            8080,
            8081,
            8888
        ):

            request = (
                f"HEAD / HTTP/1.0\r\n"
                f"Host: {target_ip}\r\n"
                f"Connection: close\r\n"
                f"\r\n"
            )

            sock.sendall(
                request.encode()
            )

            response = sock.recv(4096)

            if response:

                return response.decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

        return "Not detected"

    except (
        socket.timeout,
        ConnectionResetError,
        ConnectionRefusedError,
        OSError
    ):

        return "Not detected"

    finally:

        sock.close()


# ============================================================
# OPEN PORT ANALYSIS
# ============================================================

def analyze_open_port(
    target_ip,
    port,
    response_time
):

    service = get_service(port)

    banner = get_banner(
        target_ip,
        port
    )

    return {
        "port": port,
        "state": "OPEN",
        "protocol": "TCP",
        "service": service,
        "banner": banner,
        "response_time": response_time
    }


# ============================================================
# MAIN SCANNER
# ============================================================

def scan_target(target_ip):

    open_ports = []

    try:

        with ThreadPoolExecutor(
            max_workers=MAX_WORKERS
        ) as executor:

            # Scan in batches so that we don't create
            # 65,535 futures at the same time.

            for batch_start in range(
                START_PORT,
                END_PORT + 1,
                BATCH_SIZE
            ):

                batch_end = min(
                    batch_start + BATCH_SIZE - 1,
                    END_PORT
                )

                futures = [
                    executor.submit(
                        scan_port,
                        target_ip,
                        port
                    )
                    for port in range(
                        batch_start,
                        batch_end + 1
                    )
                ]

                for future in as_completed(
                    futures
                ):

                    result = future.result()

                    # IMPORTANT:
                    # Only OPEN ports are saved.
                    # CLOSED and FILTERED are ignored.

                    if result["state"] == "OPEN":

                        open_ports.append(
                            result
                        )

    except KeyboardInterrupt:

        print()
        print("[!] Scan stopped by user.")

        executor.shutdown(
            wait=False,
            cancel_futures=True
        )

        return

    # ========================================================
    # DETAILED ANALYSIS
    # ========================================================

    detailed_results = []

    for result in sorted(
        open_ports,
        key=lambda x: x["port"]
    ):

        detailed = analyze_open_port(
            target_ip,
            result["port"],
            result["response_time"]
        )

        detailed_results.append(
            detailed
        )

    # ========================================================
    # DISPLAY ONLY OPEN PORTS
    # ========================================================

    print()
    print("=" * 65)
    print("OPEN PORTS")
    print("=" * 65)

    if not detailed_results:

        print()
        print("No open ports found.")

    else:

        for result in detailed_results:

            print()
            print("-" * 65)

            print(
                f"Port          : "
                f"{result['port']}"
            )

            print(
                f"State         : "
                f"{result['state']}"
            )

            print(
                f"Protocol      : "
                f"{result['protocol']}"
            )

            print(
                f"Service       : "
                f"{result['service']}"
            )

            print(
                f"Response Time : "
                f"{result['response_time']:.2f} ms"
            )

            print(
                f"Version/Banner: "
                f"{result['banner']}"
            )

    print()
    print("=" * 65)


# ============================================================
# PROGRAM ENTRY
# ============================================================

def main():

    print()
    print("=" * 65)
    print("PORT SCANNER")
    print("=" * 65)
    print()

    target_ip = input(
        "Enter target IP address: "
    ).strip()

    if not validate_ip(target_ip):

        print()
        print("[!] Invalid IP address.")
        return

    scan_target(target_ip)


if __name__ == "__main__":

    try:

        main()

    except KeyboardInterrupt:

        print()
        print("[!] Scan stopped by user.")
