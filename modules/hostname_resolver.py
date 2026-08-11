import socket


def get_user_input():
    """Prompt for the hostname that should be resolved."""
    print("\n==============================")
    print("Hostname Resolver")
    print("==============================")
    hostname = input("Enter a hostname to resolve: ").strip()
    return hostname


def resolve_hostname(hostname):
    """Return the IPv4 address for *hostname* or raise a lookup error."""
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror as e:
        raise RuntimeError(
        f"Error resolving hostname '{hostname}': {e}"
    ) from e


def controller():
    """Run the interactive hostname-resolution workflow."""
    hostname = get_user_input()
    try:
        ip_address = resolve_hostname(hostname)
        print(f"\nThe IP address of '{hostname}' is: {ip_address}")
    except socket.gaierror as e:
        print(f"\n{e}")

