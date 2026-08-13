import socket
import urllib.error
import urllib.request
from urllib.parse import urlparse


def display_header():
    """Print the application banner."""
    print("\n==============================")
    print(" Web Availability Checker")
    print("==============================")


def get_website():
    """Prompt the user for a website and enforce non-empty input.

    Returns:
        str: Clean user-entered website URL or domain.
    """
    while True:
        web_name = input("Enter the website: ").strip()

        if web_name:
            return web_name

        print("Error: Website URL cannot be empty. Please try again.")


def normalize_url(web_name):
    """Normalize a website name into an HTTP/HTTPS URL.

    Args:
        web_name (str): Raw website name or URL.

    Returns:
        str: Normalized URL.

    Raises:
        ValueError: If the URL does not contain a valid hostname.
    """
    # Add HTTPS when no scheme was provided.
    if not web_name.lower().startswith(("http://", "https://")):
        web_name = f"https://{web_name}"

    parsed = urlparse(web_name)

    if not parsed.netloc:
        raise ValueError("Invalid website address. Please enter a valid domain or URL.")

    return web_name


def check_website(url):
    """Check website availability using an HTTP/HTTPS request.

    Args:
        url (str): Target website URL.

    Returns:
        dict: Response metadata.

    Raises:
        RuntimeError: If the connection fails, DNS lookup fails,
            or the request times out.
    """

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    request = urllib.request.Request(
        url,
        headers=headers,
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            return {
                "status": "Success",
                "status_code": response.getcode(),
                "reason": response.reason,
                "final_url": response.geturl(),
            }

    except urllib.error.HTTPError as e:
        # HTTP errors such as 403, 404, and 500 still mean
        # that the server responded.
        return {
            "status": "HTTP Error",
            "status_code": e.code,
            "reason": e.reason,
            "final_url": e.url,
        }

    except urllib.error.URLError as e:
        reason = e.reason

        if isinstance(reason, socket.timeout):
            raise RuntimeError(f"Connection to '{url}' timed out.") from e

        raise RuntimeError(f"Connection failed for '{url}': {reason}") from e

    except TimeoutError as e:
        raise RuntimeError(f"Connection to '{url}' timed out.") from e


def display_result(result):
    """Display structured website availability results.

    Args:
        result (dict): Website response information.
    """
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")

    status = result.get("status", "N/A")
    status_code = result.get("status_code", "N/A")
    reason = result.get("reason", "N/A")
    final_url = result.get("final_url", "N/A")

    print(f"\nStatus      : {status}")
    print(f"Status Code : {status_code}")
    print(f"Reason      : {reason}")
    print(f"Final URL   : {final_url}")


def controller():
    """Run the website availability checking workflow."""
    try:
        display_header()

        # Get user input.
        web_name = get_website()

        # Normalize and validate the URL.
        url = normalize_url(web_name)

        # Check website availability.
        result = check_website(url)

        # Display response information.
        display_result(result)

    except ValueError as e:
        print(f"\nError: {e}")

    except RuntimeError as e:
        print(f"\n{e}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
