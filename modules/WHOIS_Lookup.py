import whois


def get_domain():
    print("=" * 16)
    print("WHOIS_LookUp")
    print("=" * 16)

    domain = input("Enter domain: ").strip()
    return domain


def whois_info(domain):
    result = whois.whois(domain)
    return result


def get_first(value):
    if isinstance(value, list):
        return value[0] if value else "Not available"
    return value if value else "Not available"


def display(result):
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")

    domain_name = result.get("domain_name")
    registrar = result.get("registrar")
    country = result.get("country")
    organization = result.get("org")
    name_servers = result.get("name_servers")
    creation_date = get_first(result.get("creation_date"))
    expiration_date = get_first(result.get("expiration_date"))
    updated_date = get_first(result.get("updated_date"))

    print(
        f"Domain Name     : {domain_name}\nRegistrar       : {registrar}\nOrganization    : {organization}\nCountry         : {country}\nServer Name     : {', '.join(name_servers)}\nCreation Date   : {creation_date}\nExpiration Date : {expiration_date}\nUpdated Date    : {updated_date}"
    )


def controller():
    domain_name = get_domain()
    result = whois_info(domain_name)
    display(result)
