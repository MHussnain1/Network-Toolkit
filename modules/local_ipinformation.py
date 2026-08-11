import socket

from modules.hostname_resolver import resolve_hostname


def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" Local IP Information")
    print("==============================")


def get_local_hostname():
    """Return the hostname assigned to this computer."""
    return socket.gethostname()


def resolve_ip(hostname):
    """Resolve the local hostname to its IPv4 address."""
    return resolve_hostname(hostname)


def display_result(hostname, local_ip):
    """Display the machine hostname and local IP address."""
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")
    print(f"\nHostname : '{hostname}'")
    print(f"Local IP : {local_ip}")


def controller():
    """Run the local hostname and IP-information workflow."""
    try:
        display_header()

        hostname = get_local_hostname()
        local_ip = resolve_ip(hostname)

        display_result(hostname, local_ip)

    except RuntimeError as e:
        print(f"\n{e}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")


