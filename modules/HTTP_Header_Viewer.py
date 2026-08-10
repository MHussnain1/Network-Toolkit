import urllib.error
import urllib.request


def display_header():
    """Prints the application banner to the user interface."""
    print("=" * 16)
    print("HTTP Header Viewer")
    print("=" * 16)


def get_host():
    """Prompts the user for a hostname/URL, sanitizes input, and enforces non-empty input.

    Returns:
        str: A clean, non-empty host string.
    """
    host = ""
    # Loop until a valid, non-empty input is provided by the user
    while not host:
        host = input("Enter the host : ").strip()
        if not host:
            print("Error: Host cannot be empty. Please try again.")
    return host


def host_validation(host_name):
    """Ensures the hostname has a valid HTTP/HTTPS scheme prefix.

    Args:
        host_name (str): Raw host input string.

    Returns:
        str: Standardized URL with scheme prefix.
    """
    if host_name.lower().startswith(("https://", "http://")):
        return host_name
    return "https://" + host_name


def get_header(host_name):
    """Fetches HTTP response headers for the given target URL.

    Args:
        host_name (str): The formatted target URL.

    Returns:
        http.client.HTTPMessage: Object containing HTTP response headers.

    Raises:
        RuntimeError: If connection, DNS, or URL formatting fails.
    """
    try:
        # Include User-Agent to prevent 403 blocks from CDNs/firewalls
        request = urllib.request.Request(
            host_name, headers={"User-Agent": "Mozilla/5.0"}
        )
        # Fetch headers with a timeout threshold
        with urllib.request.urlopen(request, timeout=10) as response:
            return response.headers
    except urllib.error.HTTPError as e:
        # HTTP errors (4xx, 5xx) still return valid HTTP headers from the server
        return e.headers
    except (urllib.error.URLError, ValueError) as e:
        # Catch DNS resolution failures, connection issues, and malformed URLs
        raise RuntimeError(f"Connection failed: {e}") from e


def display(header):
    """Formats and prints selected HTTP headers to the console.

    Args:
        header (http.client.HTTPMessage): Response header collection.
    """
    # PEP 8 compliant variable names with fallbacks if a header isn't returned
    server = header.get("server", "N/A")
    content_type = header.get("Content-Type", "N/A")
    content_length = header.get("Content-Length", "N/A")
    date = header.get("Date", "N/A")
    connection = header.get("Connection", "N/A")

    # Corrected display typos ('Data' -> 'Date', 'faild' -> 'failed')
    print(
        f"\nServer         : '{server}'"
        f"\nContent Type   : '{content_type}'"
        f"\nContent Length : '{content_length}'"
        f"\nDate           : '{date}'"
        f"\nConnection     : '{connection}'"
    )


def controller():
    """Runs the interactive HTTP header viewer workflow with interrupt handling."""
    try:
        display_header()
        raw_host = get_host()
        formatted_url = host_validation(raw_host)
        header = get_header(formatted_url)
        display(header)
    except RuntimeError as e:
        print(f"\n{e}")
    except KeyboardInterrupt:
        # Handle manual exit (Ctrl+C) gracefully without throwing a traceback
        print("\n\nOperation cancelled by user.")

