import socket
from modules.hostname_resolver import resolve_hostname


def get_local_hostname():
    """Return the hostname assigned to this computer."""
    local_hostname = socket.gethostname()
    return local_hostname

def resolve_ip(hostname):
    """Resolve the supplied local hostname to its configured IPv4 address."""
    ip = resolve_hostname(hostname)
    return ip

def display_result(hostname,local_ip):
    """Display the machine hostname and resolved local IP address."""
    print("\n==============================")
    print("Results")
    print("==============================")

    print(f"\n Hostname: '{hostname}' \n local_ip : {local_ip}")
def local_ip_information():
    """Run the local hostname and IP-information workflow."""
    host_naem = get_local_hostname()
    local_ip = resolve_ip(host_naem)
    display_result(host_naem,local_ip)

