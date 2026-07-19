import socket


def get_hostname():
    print("\n==============================")
    print(" DNS Lookup")
    print("==============================")
    hostname = input("Enter a hostname to resolve: ").strip()
    return hostname


def dns_info(hostname):
    ipv4_addresses = set()
    ipv6_addresses = set()

    try:
        # Resolve the hostname to retrieve its IP addresses.
        results = socket.getaddrinfo(hostname, None)
    except socket.gaierror:
        return ipv4_addresses, ipv6_addresses

    for result in results:
        family = result[0]
        address = result[4][0]

        if family == socket.AF_INET:
            ipv4_addresses.add(address)
        elif family == socket.AF_INET6:
            ipv6_addresses.add(address)

    return ipv4_addresses, ipv6_addresses


def display(ipv4, ipv6, hostname):
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")
    print(f"\nHostname: {hostname}")
    print(f"\nThe IPv4 address is: {ipv4 if ipv4 else 'not found'}")
    print(f"\nThe IPv6 address is: {ipv6 if ipv6 else 'not found'}")


def controller():
    # Gather the hostname, resolve it, and display the result.
    hostname = get_hostname()
    ipv4, ipv6 = dns_info(hostname)
    display(ipv4, ipv6, hostname)
