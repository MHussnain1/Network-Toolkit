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
| WHOIS Lookup | Retrieves domain registration details (registrar, dates, name servers, etc.). | `modules/WHOIS_Lookup.py` |
| Web Availability Check | Checks if a website is reachable and returns the HTTP status code. | `modules/web_availability_check.py` |
| HTTP Header Viewer | Fetches and displays HTTP response headers from a given host. | `modules/HTTP_Header_Viewer.py` |

## Requirements

- Python 3.9 or later (Python 3.11+ recommended)
- An internet connection for public-IP and geolocation features
- Windows for the built-in ping workflow as currently written (`ping -n 4` is the Windows syntax)

## Dependencies

Most features rely only on Python's standard library. The **WHOIS Lookup** utility requires the external `python-whois` package:

- `python-whois==0.9.6`

Install dependencies with:

```powershell
pip install -r requirements.txt
```

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
python -c "from modules.WHOIS_Lookup import controller; controller()"
python -c "from modules.web_availability_check import controller; controller()"
python -c "from modules.HTTP_Header_Viewer import controller; controller()"
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

### Public IP

First verifies internet connectivity by establishing a socket connection to `8.8.8.8:53`. Once connectivity is confirmed, it queries the [ipify API](https://www.ipify.org/) (`https://api.ipify.org`) using Python's standard `urllib.request` to fetch and display the device's public-facing IPv4 address.

### IP Geolocation (`modules/ip_geolocation.py`)

Retrieves geolocation metadata for the user's public IP address using [ip-api.com](https://ip-api.com/).

- **Workflow**:
  1. Checks internet connectivity using `is_connected()` from `modules/public_ip.py`.
  2. Fetches the public IP address using `public_ip()` from `modules/public_ip.py`.
  3. Sends an HTTP GET request to `http://ip-api.com/json/{ip}` using Python's standard library `urllib.request`.
  4. Parses the JSON response and outputs the location details.

- **Information Displayed**:
  - **Status**: API status (`success` or `fail`)
  - **IP**: Public IP address queried
  - **Country**: Country name
  - **Region**: Region or state name (`regionName`)
  - **City**: City name
  - **Timezone**: Local timezone designation

> **Note on Privacy & External Services**: Both Public IP lookup and IP Geolocation rely on external HTTP endpoints (`ipify.org` and `ip-api.com`). Your public IP address is transmitted to these third-party services during lookup. IP geolocation is approximate and should not be treated as a precise physical location.

### WHOIS Lookup

Prompts for a domain name and uses the `python-whois` library to query domain registration information. Displays the domain name, registrar, organization, country, name servers, creation date, expiration date, and last updated date.

### Web Availability Check

Prompts for a website URL or hostname (the `https://` prefix is added automatically if missing). Uses `urllib.request.urlopen()` to send an HTTP GET request and reports the HTTP status code, reason phrase, and the final URL (after any redirects). If the request fails, a DNS resolution failure message is shown.

### HTTP Header Viewer

Prompts for a hostname (the `https://` prefix is added automatically if missing). Sends an HTTP GET request using `urllib.request.urlopen()` and displays key response headers: **Server**, **Content-Type**, **Content-Length**, **Date**, and **Connection**. If the request fails, a connection failure message is shown.

## Project structure

```text
NetworkToolKit/
├── main.py                       # Interactive menu entry point
├── requirements.txt              # Python dependencies (python-whois)
├── modules/
│   ├── hostname_resolver.py      # IPv4 hostname resolution
│   ├── port_scanner.py           # Single TCP-port check
│   ├── ping_host.py              # Windows ping workflow
│   ├── local_ipinformation.py    # Local hostname/IP display
│   ├── DNS_Lookup.py             # IPv4/IPv6 DNS lookup
│   ├── public_ip.py              # ipify public-IP lookup
│   ├── ip_geolocation.py         # ip-api geolocation lookup
│   ├── WHOIS_Lookup.py           # Domain WHOIS information
│   ├── web_availability_check.py # Website HTTP availability check
│   └── HTTP_Header_Viewer.py     # HTTP response header viewer
└── README.md
```

## Launcher

The interactive launcher (`main.py`) presents a numbered menu (1–10) and prompts for the hostname or port required by the selected utility. All imports use distinct aliases, so each menu choice correctly invokes its corresponding utility.

## Troubleshooting

| Problem | Likely cause and action |
| --- | --- |
| `python` is not recognized | Install Python and ensure it is added to `PATH`, or use the Python launcher: `py main.py`. |
| Hostname cannot be resolved | Check spelling, DNS connectivity, and whether the name has an IPv4 record. |
| Ping fails | The host may block ICMP; test a known service with the port checker if you are authorized. |
| Public IP / geolocation fails | Confirm internet access and that the external provider is reachable. |
| Ping does not work on macOS/Linux | The current command uses Windows' `-n` flag. Update it to the platform-appropriate `-c` flag before running there. |

## Contributing

Contributions are welcome. Keep additions focused, use the standard library unless a dependency is justified, and test utilities only against authorized targets. Useful future improvements include adding cross-platform ping support, setting the socket timeout before connecting, and adding automated tests.

## License

No license file is currently included. Add a license before distributing or reusing this project under defined terms.
