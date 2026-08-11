import socket
from modules.hostname_resolver import resolve_hostname
def display_header():
    """Prints the application banner to the user interface."""
    print("\n==============================")
    print(" Port Scanner")
    print("==============================")

def get_hostname():
    """Prompts the user for a hostname and enforces non-empty input.

    Returns:
        str: A clean, non-empty hostname string.
    """
    hostname = ""
    # Loop until a valid, non-empty input is provided by the user
    while not hostname:
        hostname = input("Enter a hostname: ").strip()
        if not hostname:
            print("Error: Hostname cannot be empty. Please try again.")
    return hostname

def get_port():
    """Prompts continuously until the user provides a valid TCP port number (0-65535).

    Returns:
        int: A valid TCP port number.
    """
    # Loop iteratively to avoid stack overhead from recursive function calls
    while True:
        port_input = input("Enter a port number: ").strip()
        if not port_input.isdigit():
            print("Error: Invalid input. Please enter a valid numeric port number.")
            continue

        port = int(port_input)
        if not (0 <= port <= 65535):
            print("Error: Invalid port number. Please enter a number between 0 and 65535.")
            continue

        return port

def resolve_ip(hostname):
    """Resolves a hostname to an IP address using M2's resolve_hostname function.

    Args:
        hostname (str): Target domain or host string.

    Returns:
        str: Resolved IPv4 address.
    """
    # Invoke shared resolver from M2 module (raises RuntimeError on failure)
    ip_address = resolve_hostname(hostname)
    return ip_address

def scan_port(ip, port):
    """Attempts a TCP connection to the target IP and port within a 1-second timeout.

    Args:
        ip (str): Target IP address string.
        port (int): TCP port number.

    Returns:
        bool: True if port is open, False otherwise.
    """
    # Create a standard IPv4 TCP stream socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Configure connection timeout on the socket instance BEFORE connecting
    sock.settimeout(1.0)

    try:
        # Attempt TCP connection (returns 0 on success)
        result = sock.connect_ex((ip, port))
        return result == 0
    finally:
        # Ensure socket resource is closed cleanly
        sock.close()

def display_results(ip, port, result):
    """Presents the connection attempt result to the console.

    Args:
        ip (str): Resolved target IP address.
        port (int): Target TCP port.
        result (bool): Reachability state of the target port.
    """
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")

    if result:
        print(f"\nPort {port} on {ip} is OPEN.")
    else:
        print(f"\nPort {port} on {ip} is CLOSED or UNREACHABLE.")

def controller():
    """Runs the interactive port scanning workflow with error and interrupt handling."""
    try:
        # Render application header banner
        display_header()

        # Capture validated target hostname
        hostname = get_hostname()

        # Resolve hostname first before prompting for port to avoid wasted input
        ip = resolve_ip(hostname)

        # Capture validated TCP port number
        port = get_port()

        # Perform single TCP port scan
        result = scan_port(ip, port)

        # Display scan results
        display_results(ip, port, result)

    except RuntimeError as e:
        # Catch and display resolution errors propagated from M2
        print(f"\n{e}")
    except KeyboardInterrupt:
        # Handle manual cancellation (Ctrl+C) gracefully
        print("\n\nOperation cancelled by user.")
