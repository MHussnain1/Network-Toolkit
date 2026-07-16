import socket
import subprocess
from modules.hostname_resolver import resolve_hostname


def get_hostname():
    # Prompt the user for a hostname and strip trailing whitespace
    print("\n==============================")
    print("Hostname Resolver")
    print("==============================")
    hostname = input("Enter a hostname to resolve: ").strip()
    return hostname


def resolve_ip(hostname):
    # Call the external module to resolve the hostname to an IP address
    try:
        ip = resolve_hostname(hostname)
        return ip
    except socket.gaierror as e:
        print(f"\nError: {e}")
        return None


def ping_host(ip):

    # Execute the ping command and capture its output
    result = subprocess.run(["ping", "-n", "4", ip], capture_output=True, text=True)
    # Check if the ping command executed successfully
    if result.returncode == 0:
        average_time = extract_average_response_time(result.stdout)
        return True, average_time
    else:
        return False, None


def extract_average_response_time(output):
    try:
        # Parse Windows-style ping output
        if "Average = " in output:
            _, _, number_str = output.rpartition("Average = ")
            number = int(number_str.strip().removesuffix("ms"))
            return number
        else:
            print("Unexpected error")
    except (ValueError, IndexError):
        # Return -1 if the parsing fails due to unexpected output formatting
        return -1
    return -1


def display_result(connection, time, host, ip):
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")

    if connection:
        print(f"HOST: {host}\nIP: {ip}\nStatus: Reachable\nResponse time: {time}ms")
    else:
        print("Connection unstable (Ping failed)")


def controller():
    # Main orchestration logic
    hostname = get_hostname()

    # Guard clause to ensure the user entered a hostname
    if not hostname:
        print("Error: No hostname entered.")
        return

    ip = resolve_ip(hostname)

    # Guard clause to ensure the hostname resolved successfully
    if not ip:
        print(f"Error: Could not resolve hostname '{hostname}'")
        return

    connection, response_time = ping_host(ip)
    display_result(connection, response_time, hostname, ip)
