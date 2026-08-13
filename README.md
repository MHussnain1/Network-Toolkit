# Network Toolkit

Network Toolkit is a modular Python command-line application for everyday network diagnostics and information gathering. It brings common lookup, connectivity, web, and route-inspection tasks together behind one simple interactive menu.

Built for learning and authorized troubleshooting, each feature is kept in its own module and launched through a central controller.

> **Disclaimer:** This project is intended for educational use and authorized network diagnostics only. Scan or test only systems and networks you own or are explicitly authorized to assess.

## Features

| # | Module | Summary |
| --- | --- | --- |
| 1 | Hostname Resolver | Resolves a hostname to an IPv4 address. |
| 2 | Port Scanner | Tests TCP connectivity to a specified host and port. |
| 3 | Ping Host | Uses the system ping utility to test reachability and latency. |
| 4 | Local IP Information | Shows the local hostname and resolved IP address. |
| 5 | DNS Lookup | Returns IPv4 and IPv6 addresses for a hostname. |
| 6 | Public IP Information | Retrieves the current public-facing IP address. |
| 7 | IP Geolocation | Looks up approximate location details for the public IP. |
| 8 | WHOIS Lookup | Retrieves domain-registration information. |
| 9 | Web Availability Checker | Checks whether a website is reachable over HTTP(S). |
| 10 | HTTP Header Viewer | Displays response headers from a web server. |
| 11 | SSL Certificate Viewer | Inspects a server's TLS/SSL certificate details. |
| 12 | Reverse DNS Lookup | Resolves an IP address back to a hostname where available. |
| 13 | Traceroute | Uses the system traceroute utility and parses the network path. |

## Technologies Used

- Python
- `socket`
- `subprocess`
- `urllib`
- `ssl`
- `re`
- `python-whois`
- JSON APIs

## Project Structure

```text
NetworkToolKit/
├── main.py                         # Menu, dispatch map, and application loop
├── modules/
│   ├── __init__.py                  # Marks modules as a Python package
│   ├── hostname_resolver.py         # Hostname → IPv4 resolution
│   ├── port_scanner.py              # Single TCP-port connectivity check
│   ├── ping_host.py                 # Platform-aware ping command and parsing
│   ├── local_ipinformation.py       # Local hostname and IP information
│   ├── DNS_Lookup.py                # IPv4/IPv6 DNS lookup
│   ├── public_ip.py                 # Connectivity check and public-IP API call
│   ├── ip_geolocation.py            # Public-IP geolocation API call
│   ├── WHOIS_Lookup.py              # Domain WHOIS lookup
│   ├── web_availability_check.py    # Website reachability check
│   ├── HTTP_Header_Viewer.py        # HTTP response-header display
│   ├── SSL_Certificate_Viewer.py    # TLS/SSL certificate inspection
│   ├── Reverse_DNS_Lookup.py        # IP address → hostname lookup
│   └── traceroute.py                # Platform-aware traceroute and hop parsing
├── requirements.txt                 # Third-party dependencies
├── README.md                        # Project documentation
└── .gitignore
```

The `modules/` directory contains an independent controller for each network utility; `main.py` provides the menu and routes a selected option to that controller.

### Module Structure

Each feature module follows the same lightweight pattern: helper functions gather and validate input, a network-operation function performs the lookup or request, a display function formats the result, and `controller()` coordinates the workflow. `main.py` imports these controllers and maps them to menu options 1–13.

| Module | Internal workflow / main functions |
| --- | --- |
| `hostname_resolver.py` | `get_user_input()` → `resolve_hostname()` → `controller()` |
| `port_scanner.py` | Input helpers → `resolve_ip()` → `scan_port()` → `display_results()` → `controller()` |
| `ping_host.py` | Input and IP resolution → `ping_host()` → `extract_average_response_time()` → `display_result()` → `controller()` |
| `local_ipinformation.py` | `get_local_hostname()` → `resolve_ip()` → `display_result()` → `controller()` |
| `DNS_Lookup.py` | `get_hostname()` → `dns_info()` → `display()` → `controller()` |
| `public_ip.py` | `is_connected()` → `public_ip()` → `display_result()` → `controller()` |
| `ip_geolocation.py` | Reuses public-IP helpers → `get_ip_geolocation()` → `display_result()` → `controller()` |
| `WHOIS_Lookup.py` | `get_domain()` → `whois_info()` → formatting helpers → `display_result()` → `controller()` |
| `web_availability_check.py` | `get_website()` → `normalize_url()` → `check_website()` → `display_result()` → `controller()` |
| `HTTP_Header_Viewer.py` | `get_host()` → `host_validation()` → `get_header()` → `display()` → `controller()` |
| `SSL_Certificate_Viewer.py` | `get_domain()` → `get_certificate()` → `parse_certificate()` → `display_result()` → `controller()` |
| `Reverse_DNS_Lookup.py` | `get_ip()` → `reverse_dns_lookup()` → `display_result()` → `controller()` |
| `traceroute.py` | `get_host()` → `run_traceroute()` → hop-parsing helpers → `display_result()` → `controller()` |

## Installation

1. Clone the repository.

   ```powershell
   git clone https://github.com/MHussnain1/Network-Toolkit.git
   cd Network-Toolkit
   ```

2. Create and activate a virtual environment.

   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install the requirements.

   ```powershell
   pip install -r requirements.txt
   ```

## Usage

Run the interactive application from the project root:

```powershell
python main.py
```

Example menu:

```text
==============================
      Network Toolkit
==============================
1.  Hostname Resolver
2.  Port Scanner
3.  Ping Host
...
11. SSL Certificate Viewer
12. Reverse DNS Lookup
13. Traceroute
0.  Exit

Enter your choice (0-13):
```

Select a numbered utility and provide the requested hostname, IP address, URL, or port.

## Example Output

### DNS Lookup

```text
Enter hostname: example.com

DNS Lookup Results
IPv4 addresses: {'93.184.216.34'}
IPv6 addresses: set()
```

### Traceroute

```text
Enter hostname: example.com
Tracing route to example.com [93.184.216.34]

  1    <1 ms    <1 ms    <1 ms  192.168.1.1
  2    12 ms    11 ms    13 ms  10.0.0.1
  ...
```

Actual results vary with DNS configuration, firewalls, operating system, and network conditions.

## Design and Architecture

The project follows a modular, controller-based workflow:

```text
User input → main.py menu → selected module controller → network/API operation → formatted result
```

`main.py` owns the application loop, menu display, and option-to-controller dispatch. Individual modules focus on one diagnostic responsibility, which keeps the code easier to test, extend, and debug without affecting unrelated tools.

## Error Handling

The toolkit is designed to fail clearly and return to the menu where possible. It includes input validation and handles common operational issues such as:

- Invalid menu choices, hostnames, IP addresses, URLs, and ports
- Connection timeouts and unavailable services
- DNS resolution failures
- Network and HTTP errors from local operations or external APIs
- `Ctrl+C` interruptions, with a graceful option to return to the menu or exit

## Testing

Each module was tested individually during development and then exercised through the main application menu.

Testing included valid and invalid user input, DNS resolution failures, connection timeouts, unreachable hosts, HTTP errors, SSL/TLS connection errors, missing traceroute responses, WHOIS lookup failures, and `Ctrl+C` interruption handling. All 13 modules were reviewed as part of the final development cycle.

## Learning and Project Goals

Network Toolkit was built to strengthen practical Python and networking skills, including debugging, modular programming, command-line workflows, DNS and socket operations, web requests, TLS inspection, and system-level networking concepts.

It is also a compact foundation for experimenting with better validation, cross-platform support, automated tests, and additional diagnostic tools.

## Author

[MHussnain1](https://github.com/MHussnain1)
