import subprocess
import re

def get_host():
    print("=" * 16)
    print("Traceroute")
    print("=" * 16)

    host = input("Enter domain or host: ").strip()
    return host


def traceroute(domain):
    result = subprocess.run(["tracert", domain], capture_output=True, text=True)

    lines = result.stdout.splitlines()

    hops = []

    for line in lines:
        if is_hop_line(line):
            hop = parse_hop(line)
            hops.append(hop)

    return hops


def is_hop_line(line):
    return re.match(r"\s*\d+", line) is not None


def parse_hop(line):
    match = re.match(
        r"\s*(\d+)\s+(\*|\d+)(?:\s+ms)?\s+(\*|\d+)(?:\s+ms)?\s+(\*|\d+)(?:\s+ms)?", line
    )

    if not match:
        return None

    hop = int(match.group(1))

    times = [match.group(2), match.group(3), match.group(4)]

    remaining = line[match.end() :].strip()

    if remaining == "Request timed out.":
        address = None
        hostname = None

    else:
        address_match = re.search(r"(.+)\s+\[([0-9.]+)\]", remaining)

        if address_match:
            hostname = address_match.group(1)
            address = address_match.group(2)

        else:
            hostname = None
            address = remaining

    return {"hop": hop, "times": times, "hostname": hostname, "address": address}


def format_time(time):
    if time == "*":
        return "*"
    return f"{time} ms"


def display(hops):
    print("\n==============================")
    print("Traceroute Results")
    print("==============================")

    for hop in hops:
        hop_number = hop["hop"]
        times = hop["times"]
        hostname = hop["hostname"]
        address = hop["address"]

        time_1 = format_time(times[0])
        time_2 = format_time(times[1])
        time_3 = format_time(times[2])

        if hostname:
            destination = f"{hostname} [{address}]"
        elif address:
            destination = address
        else:
            destination = "Request timed out."

        print(
            f"{hop_number:>2}   "
            f"{time_1:>7}   "
            f"{time_2:>7}   "
            f"{time_3:>7}   "
            f"{destination}"
        )

def controller():
    host = get_host()
    hops = traceroute(host)
    display(hops)
