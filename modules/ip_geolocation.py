import json
import urllib.error
import urllib.request
from modules.public_ip import is_connected, public_ip


def display_header():
    """Prints the application banner to the user interface."""
    print("\n==============================")
    print(" IP Geolocation Lookup")
    print("==============================")


def get_ip_geolocation(ip):
    """Fetches geolocation details for a given IP address using ip-api.com.

    Args:
        ip (str): The target IP address.

    Returns:
        dict: Parsed JSON geolocation data.

    Raises:
        RuntimeError: If network request or JSON parsing fails.
    """
    url = f"http://ip-api.com/json/{ip}"
    try:
        request = urllib.request.Request(
        url,
        headers={"User-Agent": "NetworkToolkit/1.0"}
)

        with urllib.request.urlopen(request, timeout=5) as response:
            data = response.read().decode()

        # Parse the JSON response body
        result = json.loads(data)
        return result
    except (urllib.error.URLError, json.JSONDecodeError, ValueError) as e:
        # Handle network failures or malformed JSON responses cleanly
        raise RuntimeError(f"Failed to fetch geolocation data: {e}") from e


def display_result(ip, result):
    """Formats and prints the IP geolocation details to the console.

    Args:
        ip (str): Resolved target IP address.
        result (dict): Geolocation data dictionary.
    """
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")

    # Validate success flag returned by the API response payload
    if result.get("status") == "success":
        print(f"\nStatus   : {result.get('status')}")
        print(f"IP       : {ip}")
        print(f"Country  : {result.get('country', 'N/A')}")
        print(f"Region   : {result.get('regionName', 'N/A')}")
        print(f"City     : {result.get('city', 'N/A')}")
        print(f"Timezone : {result.get('timezone', 'N/A')}")
    else:
        print("\nStatus   : Failed to retrieve geolocation info")


def controller():
    """Runs the IP geolocation workflow with connectivity and interrupt handling."""
    try:
        display_header()

        # Check internet connectivity before attempting the HTTP call
        if not is_connected():
            print("\nError: Internet connection is unavailable.")
            return

        ip = public_ip()
        if not ip:
            print("\nError: Could not determine public IP address.")
            return

        # Retrieve and display IP geolocation results
        result = get_ip_geolocation(ip)
        display_result(ip, result)

    except RuntimeError as e:
        print(f"\n{e}")
    except KeyboardInterrupt:
        # Handle manual cancellation (Ctrl+C) gracefully without throwing a traceback
        print("\n\nOperation cancelled by user.")


