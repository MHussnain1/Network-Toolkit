import socket
def get_user_input():
    print("\n==============================")
    print("Hostname Resolver")
    print("==============================")
    hostname = input("Enter a hostname to resolve: ")
    return hostname
def resolve_hostname(hostname):
    try:
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.gaierror as e:
        raise socket.gaierror(f"Error resolving hostname '{hostname}': {e}")
    
def hostname_resolver():
    hostname = get_user_input()
    try:
        ip_address = resolve_hostname(hostname)
        print(f"\nThe IP address of '{hostname}' is: {ip_address}")
    except socket.gaierror as e:
        print(f"\n{e}")

