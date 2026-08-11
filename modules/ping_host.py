import platform
import subprocess
from modules.hostname_resolver import resolve_hostname


def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" Ping Tool")
    print("==============================")


def get_hostname():
    """Prompt the user for a non-empty hostname."""
    hostname = ""

    while not hostname:
        hostname = input("Enter a hostname to ping: ").strip()

        if not hostname:
            print("Error: Hostname cannot be empty. Please try again.")

    return hostname


def resolve_ip(hostname):
    """Resolve a hostname to its IPv4 address."""
    return resolve_hostname(hostname)


def ping_host(ip):
    """Ping an IPv4 address four times and return reachability and average latency."""

    param = "-n" if platform.system().lower() == "windows" else "-c"

    try:
        result = subprocess.run(
            ["ping", param, "4", ip],
            capture_output=True,
            text=True,
            timeout=10,
        )

        if result.returncode == 0:
            average_time = extract_average_response_time(result.stdout)
            return True, average_time

        return False, None

    except subprocess.TimeoutExpired:
        return False, None


def extract_average_response_time(output):
    """Extract average ping latency in milliseconds."""

    try:
        # Windows format:
        # Average = 24ms
        if "Average = " in output:
            _, _, number_str = output.rpartition("Average = ")
            number_str = number_str.strip().removesuffix("ms")
            return float(number_str)

        # Linux/macOS format:
        # min/avg/max/mdev = 10.123/12.456/...
        if "min/avg/max" in output or "round-trip" in output:
            for line in output.splitlines():
                if "=" in line and "/" in line:
                    parts = line.split("=")[1].strip().split("/")

                    if len(parts) >= 2:
                        return float(parts[1])

    except (ValueError, IndexError):
        return -1

    return -1


def display_result(connection, response_time, host, ip):
    """Display the final ping result."""

    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")

    if connection:
        if response_time != -1:
            latency_str = f"{response_time:g} ms"
        else:
            latency_str = "N/A (Parsing error)"

        print(f"\nHOST          : {host}")
        print(f"IP            : {ip}")
        print("Status        : Reachable")
        print(f"Response time : {latency_str}")

    else:
        print(f"\nHOST          : {host}")
        print(f"IP            : {ip}")
        print("Status        : Unreachable (Ping failed)")


def controller():
    """Coordinate hostname resolution, pinging, and result display."""

    try:
        display_header()

        hostname = get_hostname()
        ip = resolve_ip(hostname)

        connection, response_time = ping_host(ip)

        display_result(
            connection,
            response_time,
            hostname,
            ip,
        )

    except RuntimeError as e:
        print(f"\n{e}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
