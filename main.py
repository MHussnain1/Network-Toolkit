from modules.hostname_resolver import hostname_resolver
from modules.port_scanner import port_scanner
from modules.ping_host import controller as ping_controller
from modules.local_ipinformation import local_ip_information
from modules.DNS_Lookup import controller as dns_controller
from modules.public_ip import controller as public_controller
from modules.ip_geolocation import controller as geo_controller
from modules.WHOIS_Lookup import controller as whois_controller


def main():
    while True:
        print("\n==============================")
        print(" Network Toolkit")
        print("==============================")

        print("1. Hostname Resolver")
        print("2. Port Scanner")
        print("3. Ping Host")
        print("4. Local IP information")
        print("5. DNS_LOOKUP")
        print("6. Public IP information ")
        print("7. IP_Geolocation")
        print("8. WHOIS Lookup")
        print("9. Exit")
        choice = input("\nEnter your choice (1-9): ").strip()

        if choice == "1":
            hostname_resolver()

        elif choice == "2":
            port_scanner()

        elif choice == "3":
            ping_controller()

        elif choice == "4":
            local_ip_information()

        elif choice == "5":
            dns_controller()

        elif choice == "6":
            public_controller()

        elif choice == "7":
            geo_controller()

        elif choice == "8":
            whois_controller()

        elif choice == "9":
            print("\nExiting the program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 9.")


if __name__ == "__main__":
    main()

