import socket


def display_header():
    """Prints the application banner to the user interface."""
    print("\n==============================")
    print(" Reverse DNS Lookup")
    print("==============================")


def get_ip():
    """Prompts the user for an IP address and enforces non-empty input.

    Returns:
        str: A clean, non-empty IP address string.
    """
    ip = ""
    # Loop until a valid, non-empty input is provided by the user
    while not ip:
        ip = input("Enter an IP address: ").strip()
        if not ip:
            print("Error: IP address cannot be empty. Please try again.")
    return ip


def reverse_dns_lookup(ip):
    """Performs a reverse DNS lookup for the given IP address.

    Args:
        ip (str): Target IPv4 or IPv6 address string.

    Returns:
        tuple: A tuple containing (primary_hostname, aliases_list, ip_addresses_list).

    Raises:
        RuntimeError: If reverse lookup fails due to an invalid IP or missing PTR record.
    """
    try:
        # Perform reverse DNS lookup using system socket API
        hostname, aliases, ip_addresses = socket.gethostbyaddr(ip)
        return hostname, aliases, ip_addresses
    except (socket.herror, socket.gaierror, OSError, ValueError) as e:
        # Catch lookup errors, invalid IP strings, or socket failures cleanly
        raise RuntimeError(
            f"Error performing reverse DNS lookup for '{ip}': {e}"
        ) from e


def display_result(hostname, aliases, ip_addresses):
    """Formats and prints reverse DNS lookup results to the console.

    Args:
        hostname (str): Primary domain/host name.
        aliases (list): List of alias hostnames.
        ip_addresses (list): List of associated IP addresses.
    """
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")
    print(f"\nHostname     : {hostname}")
    print(f"Aliases      : {aliases}")
    print(f"IP Addresses : {ip_addresses}")


def controller():
    """Runs the reverse DNS lookup workflow with error and interrupt handling."""
    try:
        # Render application header banner
        display_header()

        # Capture validated IP address input
        ip_address = get_ip()

        # Execute reverse DNS lookup
        hostname, aliases, ip_addresses = reverse_dns_lookup(ip_address)

        # Display resolved reverse DNS details
        display_result(hostname, aliases, ip_addresses)

    except RuntimeError as e:
        # Catch and display lookup errors cleanly
        print(f"\n{e}")
    except KeyboardInterrupt:
        # Handle manual exit (Ctrl+C) gracefully without throwing a traceback
        print("\n\nOperation cancelled by user.")
