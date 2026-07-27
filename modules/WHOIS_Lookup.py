import whois


def get_domain():
    print("="*16)
    print("WHOIS_LookUp" )
    print("="*16)

    domain = input("Enter domain: ").strip()
    return domain

def whois_info(domain):
    result = whois.whois(domain)
    return result

def display(result):
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")
    domain_name = result.get("domain_name")
    registrar = result.get("registrar")
    country = result.get("country")
    creation_date = result.get("creation_date")[0] if result.get("creation_date") else "Not available"
    expiration_date = result.get("expiration_date")[0] if result.get("expiration_date") else "Not available"
    updated_date = result.get("updated_date")[0] if result.get("updated_date") else "Note Available"

    print(f"\n domain_name: '{domain_name}' \n registrar : '{registrar}' \n country : '{country}' \n creation date : '{creation_date}'\n expiration date : '{expiration_date}'\n update date : {updated_date}")



def controller():
    domain_name = get_domain()
    result = whois_info(domain_name)
    display(result)
