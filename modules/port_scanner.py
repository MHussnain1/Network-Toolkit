import socket
from modules.hostname_resolver import resolve_hostname


def get_hostname():
    """Prompt for the host whose port will be checked."""
    print("\n==============================")
    print("Port Scanner")
    print("==============================")

    hostname = input("Enter a hostname: ").strip()
    return hostname


def get_port():
    """Prompt until the user provides a valid TCP port number."""
    port_input = input("Enter a port number: ").strip()
    if not port_input.isdigit():
        print("\nInvalid input. Please enter a valid port number.")
        return get_port()  
    if not (0 <= int(port_input) <= 65535):
        print("\nInvalid port number. Please enter a number between 0 and 65535.")
        return get_port()  
    return int(port_input)


def resolve_ip(hostname):
    """Resolve a hostname for scanning and report lookup failures to the user."""
    try:
        ip_address = resolve_hostname(hostname)
        return ip_address
    except socket.gaierror as e:
        print(f"\nError resolving hostname '{hostname}': {e}")
        return None


def scan_port(ip, port):
    """Return whether a TCP connection to the given address and port succeeds."""
    if ip is None:
        print("\nCannot scan ports because the IP address could not be resolved.")
        return False
    # Use TCP because port availability is determined by a TCP connection attempt.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        result = sock.connect_ex((ip, port))
    finally:
        sock.close()
    socket.setdefaulttimeout(1)  
    if result == 0:
        return True
    else:
        return False


def display_results(ip, port, result):
    """Present the connection-attempt outcome."""
    if result:
        print(f"\nPort {port} on {ip} is open.")
    else:
        print(f"\nPort {port} on {ip} is closed.")


def port_scanner():
    """Run the interactive single-port scanning workflow."""
    ip = resolve_ip(get_hostname())
    port = get_port()
    result = scan_port(ip, port)
    display_results(ip, port, result)
