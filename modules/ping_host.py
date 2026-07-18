import socket
import subprocess
from modules.hostname_resolver import resolve_hostname


def get_hostname():
    """Prompt for the hostname that should be pinged."""
    print("\n==============================")
    print("Hostname Resolver")
    print("==============================")
    hostname = input("Enter a hostname to resolve: ").strip()
    return hostname


def resolve_ip(hostname):
    """Resolve a hostname before passing it to the system ping command."""
    try:
        ip = resolve_hostname(hostname)
        return ip
    except socket.gaierror as e:
        print(f"\nError: {e}")
        return None


def ping_host(ip):
    """Ping an IPv4 address four times and return reachability and average latency."""
    # `-n` is the Windows flag that controls the number of echo requests.
    result = subprocess.run(["ping", "-n", "4", ip], capture_output=True, text=True)
    if result.returncode == 0:
        average_time = extract_average_response_time(result.stdout)
        return True, average_time
    else:
        return False, None


def extract_average_response_time(output):
    """Extract the average latency from Windows `ping` output, if available."""
    try:
        if "Average = " in output:
            _, _, number_str = output.rpartition("Average = ")
            number = int(number_str.strip().removesuffix("ms"))
            return number
        else:
            print("Unexpected error")
    except (ValueError, IndexError):
        # Ping output can vary with locale or platform, so parsing is best-effort.
        return -1
    return -1


def display_result(connection, time, host, ip):
    """Print the final reachability result for the requested host."""
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")

    if connection:
        print(f"HOST: {host}\nIP: {ip}\nStatus: Reachable\nResponse time: {time}ms")
    else:
        print("Connection unstable (Ping failed)")


def controller():
    """Coordinate input, hostname resolution, pinging, and output."""
    hostname = get_hostname()

    if not hostname:
        print("Error: No hostname entered.")
        return

    ip = resolve_ip(hostname)

    if not ip:
        print(f"Error: Could not resolve hostname '{hostname}'")
        return

    connection, response_time = ping_host(ip)
    display_result(connection, response_time, hostname, ip)
