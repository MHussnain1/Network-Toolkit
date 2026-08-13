import platform
import re
import subprocess
from urllib.parse import urlparse


def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" Traceroute Tool")
    print("==============================")


def get_host():
    """Prompt for a target host or domain and sanitize the input.

    Returns:
        str: Clean target hostname or IP address.
    """
    host_input = ""

    while not host_input:
        host_input = input("Enter domain or host: ").strip()

        if not host_input:
            print("Error: Host cannot be empty. Please try again.")

    # Remove URL scheme if the user enters a complete URL.
    if "://" in host_input:
        parsed = urlparse(host_input)
        host_input = parsed.netloc or parsed.path

    # Remove path and explicit port.
    host = host_input.split("/")[0].split(":")[0]

    return host


def is_hop_line(line):
    """Determine whether a line represents a traceroute hop."""
    return re.match(r"^\s*\d+\s+", line) is not None


def parse_hop(line):
    """Parse one traceroute hop line into structured data.

    Args:
        line (str): Raw traceroute output line.

    Returns:
        dict | None: Parsed hop information.
    """

    # Extract hop number.
    hop_match = re.match(r"^\s*(\d+)\s+", line)

    if not hop_match:
        return None

    hop = int(hop_match.group(1))

    # Remove hop number from the line.
    remaining = line[hop_match.end():].strip()

    times = []

    # Extract up to three probe results.
    for _ in range(3):
        time_match = re.match(
            r"(\*|<1|\d+)(?:\s*ms)?\s*",
            remaining
        )

        if not time_match:
            break

        times.append(time_match.group(1))
        remaining = remaining[time_match.end():].strip()

    # Handle a completely timed-out hop.
    if not remaining or remaining == "Request timed out.":
        hostname = None
        address = None

    else:
        # Example:
        # lcmcta-ai-in-f14.1e100.net [142.250.202.206]
        address_match = re.search(
            r"(.+?)\s+\[([0-9a-fA-F:.]+)\]",
            remaining
        )

        if address_match:
            hostname = address_match.group(1).strip()
            address = address_match.group(2)

        else:
            # Destination may be a plain IPv4/IPv6 address.
            hostname = None
            address = remaining.strip()

    return {
        "hop": hop,
        "times": times,
        "hostname": hostname,
        "address": address,
    }

def run_traceroute(domain):
    """Execute the platform-specific traceroute command.

    Args:
        domain (str): Target hostname or IP address.

    Returns:
        list: Parsed traceroute hop dictionaries.

    Raises:
        RuntimeError: If traceroute cannot be executed or times out.
    """

    if platform.system().lower() == "windows":
        command = "tracert"

        # Limit Windows traceroute to 15 hops and wait
        # up to 2 seconds for each response.
        command_args = [
            command,
            "-h",
            "15",
            "-w",
            "2000",
            domain,
        ]

    else:
        command = "traceroute"

        command_args = [
            command,
            "-m",
            "15",
            "-w",
            "2",
            domain,
        ]

    try:
        result = subprocess.run(
            command_args,
            capture_output=True,
            text=True,
            timeout=60,
        )

    except FileNotFoundError:
        raise RuntimeError(
            f"Command '{command}' not found on the system."
        )

    except subprocess.TimeoutExpired:
        raise RuntimeError(
            f"Traceroute operation to '{domain}' timed out after 60 seconds."
        )

    except subprocess.SubprocessError as e:
        raise RuntimeError(
            f"Failed to execute traceroute for '{domain}': {e}"
        ) from e

    if result.returncode != 0 and not result.stdout:
        error = result.stderr.strip() or "Unknown error."

        raise RuntimeError(
            f"Traceroute failed for '{domain}': {error}"
        )

    lines = result.stdout.splitlines()

    hops = []

    for line in lines:
        if is_hop_line(line):
            hop_data = parse_hop(line)

            if hop_data is not None:
                hops.append(hop_data)

    return hops


def format_time(time_val):
    """Format an individual probe latency."""

    if time_val == "*":
        return "*"

    if time_val == "<1":
        return "<1 ms"

    return f"{time_val} ms"


def display_result(hops):
    """Display structured traceroute results."""

    print("\n---------------------------")
    print("\n==============================")
    print(" Traceroute Results")
    print("==============================")

    if not hops:
        print("\nNo traceroute hop data recorded.")
        return

    print(
        "\nHop    Probe 1    Probe 2    Probe 3    Destination"
    )
    print("-" * 70)

    for hop in hops:

        hop_number = hop["hop"]
        times = hop.get("times", [])

        hostname = hop.get("hostname")
        address = hop.get("address")

        # Always display three probe columns.
        padded_times = times + ["*"] * (3 - len(times))

        time_1 = format_time(padded_times[0])
        time_2 = format_time(padded_times[1])
        time_3 = format_time(padded_times[2])

        # Determine destination display.
        if hostname and address:
            destination = f"{hostname} [{address}]"

        elif address:
            destination = address

        else:
            destination = "Request timed out."

        print(
            f"{hop_number:>3}    "
            f"{time_1:>8}   "
            f"{time_2:>8}   "
            f"{time_3:>8}    "
            f"{destination}"
        )


def controller():
    """Run the traceroute workflow."""

    try:
        display_header()

        # Get and sanitize target host.
        host = get_host()

        # Execute traceroute and parse its output.
        hops = run_traceroute(host)

        # Display parsed results.
        display_result(hops)

    except RuntimeError as e:
        print(f"\n{e}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")