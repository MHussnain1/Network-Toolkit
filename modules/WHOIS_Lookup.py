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




def controller():
    domain_name = get_domain()
    result = whois_info(domain_name)
    print(result)