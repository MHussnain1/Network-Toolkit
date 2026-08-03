import socket

def get_ip():
    print("=" * 16)
    print("Reverse DNS Lookup")
    print("=" * 16)

    ip = input("Enter ip address : ").strip()
    return ip


def reverse_dns_lookup(ip):
    try:
        hostname = socket.gethostbyaddr(ip)
        return {"status": "success", "hostname": hostname}
    except (socket.herror, socket.gaierror):
        return {
            "status": "error",
            "message": "No hostname found for the given IP address.",
        }


def display(result):
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")
    if result["status"] == "success":
        print(f"Hostname: {result['hostname'][0]}")
        print(f"aliases: {result['hostname'][1]}")
        print(f"IP addresses: {result['hostname'][2]}")
    else:
        print(f"Error: No hostname found for the given IP address.")


def controller():
    ip_address = get_ip()
    result = reverse_dns_lookup(ip_address)
    display(result)

















































































