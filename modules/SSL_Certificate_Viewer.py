import socket
import ssl
from urllib.parse import urlparse


def display_header():
    """Prints the application banner to the user interface."""
    print("\n==============================")
    print(" SSL Certificate Viewer")
    print("==============================")


def get_domain():
    """Prompts the user for a domain name, enforces non-empty input, and sanitizes input strings.

    Returns:
        str: A clean, sanitized target domain hostname.
    """
    domain_input = ""
    # Loop until valid non-empty input is provided by the user
    while not domain_input:
        domain_input = input("Enter the domain: ").strip()
        if not domain_input:
            print("Error: Domain cannot be empty. Please try again.")

    # Strip URI scheme (http:// or https://) if entered by user
    if "://" in domain_input:
        parsed = urlparse(domain_input)
        domain_input = parsed.netloc or parsed.path

    # Clean any trailing paths, slashes, or explicit port numbers
    domain = domain_input.split("/")[0].split(":")[0]
    return domain


def get_certificate(domain):
    """Retrieves the raw SSL/TLS certificate dictionary for a target domain over port 443.

    Args:
        domain (str): Target domain hostname.

    Returns:
        dict: Parsed peer certificate dictionary from the SSL context.

    Raises:
        RuntimeError: If socket connection, SSL handshake, or DNS resolution fails.
    """
    try:
        # Create standard default SSL context
        context = ssl.create_default_context()

        # Double context manager guarantees clean socket closure without finally block bugs
        with socket.create_connection((domain, 443), timeout=5) as connection:
            with context.wrap_socket(connection, server_hostname=domain) as secure_socket:
                # Extract peer certificate metadata dictionary
                certificate = secure_socket.getpeercert()
                if not certificate:
                    raise RuntimeError("No SSL certificate returned by server.")
                return certificate

    except (ssl.SSLError, socket.gaierror, socket.timeout, OSError, ValueError) as e:
        # Wrap network, DNS, and SSL exceptions into a unified RuntimeError
        raise RuntimeError(f"Failed to retrieve SSL certificate for '{domain}': {e}") from e


def parse_certificate(certificate):
    """Extracts relevant metadata fields from the raw SSL certificate dictionary.

    Args:
        certificate (dict): Raw certificate dictionary from getpeercert().

    Returns:
        dict: Processed key details including subject, issuer, validity dates, and serial.
    """
    # Convert certificate subject and issuer tuple pairs into flat dictionaries
    subject = dict(x[0] for x in certificate.get("subject", []))
    issuer = dict(x[0] for x in certificate.get("issuer", []))

    # Extract key attributes with fallback defaults
    return {
        "Common Name": subject.get("commonName", "N/A"),
        "Organization": issuer.get("organizationName", "N/A"),
        "Country": issuer.get("countryName", "N/A"),
        "Serial Number": certificate.get("serialNumber", "N/A"),
        "Not Before": certificate.get("notBefore", "N/A"),
        "Not After": certificate.get("notAfter", "N/A"),
    }


def display_result(parsed_cert):
    """Prints the structured SSL certificate details to the console.

    Args:
        parsed_cert (dict): Parsed key-value metadata dictionary.
    """
    print("\n---------------------------")
    print("\n==============================")
    print(" Results")
    print("==============================")

    # Output formatted certificate information
    for key, value in parsed_cert.items():
        print(f"\n{key:<14}: {value}")


def controller():
    """Runs the SSL certificate retrieval workflow with error and interrupt handling."""
    try:
        # Render application header banner
        display_header()

        # Capture and sanitize user domain input
        domain = get_domain()

        # Retrieve raw peer certificate over TLS
        certificate = get_certificate(domain)

        # Parse key fields from certificate dictionary
        parsed_cert = parse_certificate(certificate)

        # Display formatted results
        display_result(parsed_cert)

    except RuntimeError as e:
        # Catch and display network/SSL errors cleanly
        print(f"\n{e}")
    except KeyboardInterrupt:
        # Handle manual exit (Ctrl+C) gracefully without throwing a traceback
        print("\n\nOperation cancelled by user.")
