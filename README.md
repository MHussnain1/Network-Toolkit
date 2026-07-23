# NetworkToolKit

NetworkToolKit is a small, interactive Python command-line toolkit for common network diagnostics. It uses Python's standard library to resolve names, check a TCP port, ping a host, inspect local and public IP addresses, perform DNS lookup, and locate the current public IP.

> Use these tools only against systems and networks you own or are authorized to test.

## Features

| Utility | What it does | Module |
| --- | --- | --- |
| Hostname Resolver | Resolves a hostname to one IPv4 address. | `modules/hostname_resolver.py` |
| Port Scanner | Attempts a TCP connection to one specified port (0–65535). | `modules/port_scanner.py` |
| Ping Host | Resolves a host, sends four ICMP echo requests, and reports average latency. | `modules/ping_host.py` |
| Local IP Information | Displays the computer hostname and its resolved IPv4 address. | `modules/local_ipinformation.py` |
| DNS Lookup | Lists the IPv4 and IPv6 addresses returned for a hostname. | `modules/DNS_Lookup.py` |
| Public IP | Retrieves the public-facing IP address. | `modules/public_ip.py` |
| IP Geolocation | Looks up country, region, city, and timezone for the current public IP. | `modules/ip_geolocation.py` |

## Requirements

- Python 3.9 or later (Python 3.11+ recommended)
- An internet connection for public-IP and geolocation features
- Windows for the built-in ping workflow as currently written (`ping -n 4` is the Windows syntax)

There are no third-party Python dependencies. `requirements.txt` is intentionally empty because the project relies only on the standard library.

## Installation

Clone or download the repository, then run the program from its root directory:

```powershell
git clone <your-repository-url>
cd NetworkToolKit
python main.py
```

Optionally, create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python main.py
```

## Using the toolkit

The interactive launcher is `main.py`. It presents a numbered menu and prompts for the hostname or port required by the selected utility.

Typical inputs include:

```text
Hostname: example.com
Port: 443
```

### Run a utility directly

Every feature can also be started directly from Python. This is useful for automation, development, or when you want to run one tool by itself.

```powershell
python -c "from modules.hostname_resolver import hostname_resolver; hostname_resolver()"
python -c "from modules.port_scanner import port_scanner; port_scanner()"
python -c "from modules.ping_host import controller; controller()"
python -c "from modules.local_ipinformation import local_ip_information; local_ip_information()"
python -c "from modules.DNS_Lookup import controller; controller()"
python -c "from modules.public_ip import controller; controller()"
python -c "from modules.ip_geolocation import controller; controller()"
```

## How each feature works

### Hostname Resolver

Prompts for a hostname and calls `socket.gethostbyname()` to return one IPv4 address. Invalid or unresolvable hostnames are reported as lookup errors.

### Port Scanner

Prompts for a hostname and a single TCP port. The hostname is resolved first, then the toolkit uses `socket.connect_ex()` to test whether a TCP connection can be established. A successful connection is reported as **open**; any unsuccessful connection is reported as **closed**.

This is a single-port TCP connectivity check, not a multi-port scanner and not a UDP scanner. Firewalls, filtering, unreachable hosts, or service policies can also cause a port to be reported as closed.

### Ping Host

Resolves a hostname to IPv4, runs the Windows `ping` command four times, and displays whether the host was reachable and the average response time. Ping can be blocked even when a service is otherwise available.

### Local IP Information

Gets the computer name with `socket.gethostname()` and resolves it to an IPv4 address. On hosts with multiple interfaces, VPNs, or unusual hostname configuration, the displayed address may not be the interface you expect.

### DNS Lookup

Uses `socket.getaddrinfo()` to collect all returned IPv4 and IPv6 addresses for a hostname. The output is displayed as Python sets, so the order is not guaranteed.

### Public IP and geolocation

The public-IP utility first checks connectivity by opening a short connection to `8.8.8.8:53`, then requests the address from [ipify](https://www.ipify.org/). The geolocation utility sends that address to [ip-api.com](https://ip-api.com/) and displays the returned country, region, city, and timezone.

These two functions require external network services. Your public IP address is sent to the relevant provider when you use them; review those providers' terms and privacy practices before use. IP geolocation is approximate and should not be treated as a precise physical location.

## Project structure

```text
NetworkToolKit/
├── main.py                       # Interactive menu entry point
├── requirements.txt              # Empty: standard-library-only project
├── modules/
│   ├── hostname_resolver.py      # IPv4 hostname resolution
│   ├── port_scanner.py           # Single TCP-port check
│   ├── ping_host.py              # Windows ping workflow
│   ├── local_ipinformation.py    # Local hostname/IP display
│   ├── DNS_Lookup.py             # IPv4/IPv6 DNS lookup
│   ├── public_ip.py              # ipify public-IP lookup
│   └── ip_geolocation.py         # ip-api geolocation lookup
└── README.md
```

## Current launcher limitation

The modules are complete and can be run directly as shown above. In the present `main.py`, several imports share the generic name `controller`, so later imports overwrite earlier ones. As a result, menu choices 3–7 currently invoke the IP-geolocation controller rather than their corresponding utilities; choice 8 exits. This README documents the intended menu utilities and provides direct commands until the launcher imports are given distinct aliases.

## Troubleshooting

| Problem | Likely cause and action |
| --- | --- |
| `python` is not recognized | Install Python and ensure it is added to `PATH`, or use the Python launcher: `py main.py`. |
| Hostname cannot be resolved | Check spelling, DNS connectivity, and whether the name has an IPv4 record. |
| Ping fails | The host may block ICMP; test a known service with the port checker if you are authorized. |
| Public IP / geolocation fails | Confirm internet access and that the external provider is reachable. |
| Ping does not work on macOS/Linux | The current command uses Windows' `-n` flag. Update it to the platform-appropriate `-c` flag before running there. |

## Contributing

Contributions are welcome. Keep additions focused, use the standard library unless a dependency is justified, and test utilities only against authorized targets. Useful future improvements include fixing the controller-name collision in `main.py`, adding cross-platform ping support, setting the socket timeout before connecting, and adding automated tests.

## License

No license file is currently included. Add a license before distributing or reusing this project under defined terms.
