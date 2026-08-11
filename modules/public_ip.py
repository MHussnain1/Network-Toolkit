import json
import socket
import urllib.error
import urllib.request


def display_header():
    """Prints the application banner to the user interface."""
    print("\n==============================")
    print(" Public IP Checker")
    print("==============================")


def is_connected():
    """Checks basic network reachability by attempting a socket connection to a public DNS server."""
    try:
        # Attempt socket connection to Google DNS on port 53 with a 3-second timeout
        with socket.create_connection(("8.8.8.8", 53), timeout=3):
            return True
    except OSError:
        return False


def public_ip():
    """Fetches the current public IPv4 address using the ipify API.

    Returns:
        str: Public IP address string.

    Raises:
        RuntimeError: If HTTP request, network connection, or JSON parsing fails.
    """
    url = "https://api.ipify.org?format=json"
    try:
        # Add User-Agent header to prevent blocking by CDNs/firewalls
        request = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0"}
        )
        # Context manager ensures the HTTP socket connection is closed cleanly
        with urllib.request.urlopen(request, timeout=5) as response:
            data = response.read().decode()

        # Parse the JSON response body
        result = json.loads(data)
        return result["ip"]
    except (urllib.error.URLError, json.JSONDecodeError, KeyError, ValueError) as e:
        # Handle connection errors, timeouts, or malformed JSON payloads cleanly
        raise RuntimeError(f"Failed to retrieve public IP address: {e}") from e


def display_result(ip):
    """Formats and prints the public IP address result to the console.

    Args:
        ip (str): Resolved public IP address.
    """
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")
    print(f"\nThe public IP is: {ip}")


def controller():
    """Runs the public IP lookup workflow with connectivity check and interrupt handling."""
    try:
        # Render application header banner
        display_header()

        # Check internet connectivity before attempting HTTP call
        if not is_connected():
            print("\nError: Internet connection is unavailable.")
            return

        # Fetch public IP address
        ip = public_ip()

        # Display resolved public IP
        display_result(ip)

    except RuntimeError as e:
        # Catch and display errors propagated from public_ip execution
        print(f"\n{e}")
    except KeyboardInterrupt:
        # Handle manual exit (Ctrl+C) gracefully without throwing a traceback
        print("\n\nOperation cancelled by user.")