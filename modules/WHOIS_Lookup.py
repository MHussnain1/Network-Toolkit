import socket
from urllib.parse import urlparse
import whois


def display_header():
    """Prints the application banner to the user interface."""
    print("\n==============================")
    print(" WHOIS Lookup")
    print("==============================")


def get_domain():
    """Prompts the user for a domain name, enforces non-empty input, and sanitizes URLs.

    Returns:
        str: A clean, sanitized target domain hostname.
    """
    domain_input = ""
    # Loop until valid non-empty input is provided by the user
    while not domain_input:
        domain_input = input("Enter domain: ").strip()
        if not domain_input:
            print("Error: Domain cannot be empty. Please try again.")

    # Strip URI scheme (http:// or https://) if entered by user
    if "://" in domain_input:
        parsed = urlparse(domain_input)
        domain_input = parsed.netloc or parsed.path

    # Clean any trailing paths, slashes, or explicit port numbers
    domain = domain_input.split("/")[0].split(":")[0]
    return domain


def whois_info(domain):
    """Performs a WHOIS query for a given domain using python-whois.

    Args:
        domain (str): Clean target domain name.

    Returns:
        dict: Raw WHOIS lookup result object/dictionary.

    Raises:
        RuntimeError: If lookup fails due to network, socket, or parser errors.
    """
    try:
        # Query WHOIS server for target domain details
        result = whois.whois(domain)

        # Ensure a result object was returned and domain_name exists
        if not result or not result.get("domain_name"):
            raise RuntimeError(f"No WHOIS record found for domain '{domain}'.")

        return result
    except (whois.parser.PywhoisError, socket.gaierror, socket.timeout, OSError, Exception) as e:
        # Wrap unexpected WHOIS parser or network errors in a unified RuntimeError
        raise RuntimeError(f"Failed to perform WHOIS lookup for '{domain}': {e}") from e


def format_field(value):
    """Normalizes raw WHOIS values (strings, lists, datetimes, None) into clean display strings.

    Args:
        value (Any): Raw value extracted from WHOIS payload.

    Returns:
        str: Formatted string value or 'N/A' fallback.
    """
    if value is None:
        return "N/A"

    # If value is a list, extract the first entry to avoid raw list printing
    if isinstance(value, list):
        if not value:
            return "N/A"
        value = value[0]

    return str(value).strip() if str(value).strip() else "N/A"


def format_name_servers(name_servers):
    """Safely formats name servers list or single string value into a clean comma-separated string.

    Args:
        name_servers (Union[list, str, None]): Name server data from WHOIS payload.

    Returns:
        str: Comma-separated name server list or 'N/A'.
    """
    if not name_servers:
        return "N/A"

    if isinstance(name_servers, list):
        # Clean non-empty items and join safely
        cleaned_ns = [str(ns).strip().lower() for ns in name_servers if ns]
        return ", ".join(cleaned_ns) if cleaned_ns else "N/A"

    return str(name_servers).strip().lower()


def display_result(result):
    """Formats and displays structured WHOIS query results to the console.

    Args:
        result (dict): Raw WHOIS result object.
    """
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")

    # Extract and normalize WHOIS fields cleanly
    domain_name = format_field(result.get("domain_name"))
    registrar = format_field(result.get("registrar"))
    organization = format_field(result.get("org"))
    country = format_field(result.get("country"))
    name_servers = format_name_servers(result.get("name_servers"))
    creation_date = format_field(result.get("creation_date"))
    expiration_date = format_field(result.get("expiration_date"))
    updated_date = format_field(result.get("updated_date"))

    # Output individual field lines cleanly instead of a monolithic block
    print(f"Domain Name   : {domain_name}")
    print(f"Registrar     : {registrar}")
    print(f"Organization  : {organization}")
    print(f"Country       : {country}")
    print(f"Name Servers  : {name_servers}")
    print(f"Creation Date : {creation_date}")
    print(f"Expiration    : {expiration_date}")
    print(f"Updated Date  : {updated_date}")


def controller():
    """Runs the WHOIS lookup workflow with error and interrupt handling."""
    try:
        # Render application header banner
        display_header()

        # Capture and sanitize user domain input
        domain = get_domain()

        # Perform WHOIS lookup query
        result = whois_info(domain)

        # Display structured results
        display_result(result)

    except RuntimeError as e:
        # Catch and display network/WHOIS errors cleanly
        print(f"\n{e}")
    except KeyboardInterrupt:
        # Handle manual exit (Ctrl+C) gracefully without throwing a traceback
        print("\n\nOperation cancelled by user.")