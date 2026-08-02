import ssl
import socket

def get_domain():
    print("=" * 16)
    print("SSL Certificate Viewer")
    print("=" * 16)
    domain = input("Enter the domain : ")
    return domain

def get_certificate(domain):
    try:
        connection = socket.create_connection((domain, 443))
        context = ssl.create_default_context()
        secure_socket = context.wrap_socket(connection, server_hostname=domain)
        certificate = secure_socket.getpeercert()
        return certificate

    except ssl.SSLError as e:
        print(f"SSL error occurred: {e}")
        return None
    finally:
        if secure_socket is not None:
            secure_socket.close()
        elif connection is not None:
            connection.close()

def certificate_analyser(certificate):
    if certificate:
        subject = dict(x[0] for x in certificate.get("subject", []))
        issuer = dict(x[0] for x in certificate.get("issuer", []))
        not_before = certificate.get("notBefore")
        not_after = certificate.get("notAfter")
        serial_number = certificate.get("serialNumber")
        result = {
            "Common Name": subject.get("commonName"),
            "Organization": issuer.get("organizationName"),
            "Country": issuer.get("countryName"),
            "Serial Number": serial_number,
            "Not Before": not_before,
            "Not After": not_after,
        }
        return result
    else:
        return {"error": "Failed to retrieve certificate information."}

def display(result):
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")

    if "error" in result:
        print(result["error"])
    else:
        for key, value in result.items():
            print(f"{key}: {value}")

def controller():
    domain = get_domain()
    certificate = get_certificate(domain)
    result = certificate_analyser(certificate)
    display(result)
