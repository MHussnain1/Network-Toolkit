import socket

def display_header():
    """Prints the application banner to the user interface."""
    print("\n==============================")
    print(" DNS Lookup")
    print("==============================")


def get_hostname():
    """Prompts the user for a hostname and enforces non-empty input.

    Returns:
        str: A clean, non-empty hostname string.
    """
    hostname = ""
    # Loop until a valid, non-empty input is provided by the user
    while not hostname:
        hostname = input("Enter a hostname to resolve: ").strip()
        if not hostname:
            print("Error: Hostname cannot be empty. Please try again.")
    return hostname


def dns_info(hostname):
    """Resolves a given hostname into sets of unique IPv4 and IPv6 addresses.

    Args:
        hostname (str): The domain name or host string to resolve.

    Returns:
        tuple[set, set]: Sets containing resolved IPv4 and IPv6 addresses.
    """
    ipv4_addresses = set()
    ipv6_addresses = set()

    try:
        # Retrieve address info (family, socket type, proto, canonname, sockaddr)
        results = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        # Gracefully handle unknown hostnames or DNS lookup errors
        return ipv4_addresses, ipv6_addresses

    # Parse through the socket results and map IPs to their respective families
    for result in results:
        family = result[0]
        address = result[4][0]  # Extracts the IP string from the address tuple

        if family == socket.AF_INET:
            ipv4_addresses.add(address)
        elif family == socket.AF_INET6:
            ipv6_addresses.add(address)

    return ipv4_addresses, ipv6_addresses


def display(ipv4_addresses, ipv6_addresses, hostname):
    """Formats and prints the DNS resolution results to the console.

    Args:
        ipv4_addresses (set): Resolved IPv4 address strings.
        ipv6_addresses (set): Resolved IPv6 address strings.
        hostname (str): The resolved host string.
    """
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")
    print(f"\nHostname: {hostname}")

    # Fallback to 'not found' if the set is empty
    print(f"\nIPv4 addresses: {ipv4_addresses if ipv4_addresses else 'not found'}")
    print(f"\nIPv6 addresses: {ipv6_addresses if ipv6_addresses else 'not found'}")


def controller():
    """Main function orchestrating execution flow across the module."""
    display_header()
    hostname = get_hostname()

    # Perform address resolution
    ipv4_addresses, ipv6_addresses = dns_info(hostname)

    # Render results to the user
    display(ipv4_addresses, ipv6_addresses, hostname)
