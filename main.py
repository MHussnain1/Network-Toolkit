import sys

# Import module controllers with aliased names for consistency
try:
    from modules.DNS_Lookup import controller as dns_controller
    from modules.HTTP_Header_Viewer import controller as header_controller
    from modules.ip_geolocation import controller as geo_controller
    from modules.local_ipinformation import controller as ipinfo_controller
    from modules.ping_host import controller as ping_controller
    from modules.port_scanner import controller as port_controller
    from modules.public_ip import controller as public_controller
    from modules.Reverse_DNS_Lookup import controller as reverse_dns_controller
    from modules.SSL_Certificate_Viewer import controller as ssl_controller
    from modules.traceroute import controller as traceroute_controller
    from modules.web_availability_check import controller as avail_controller
    from modules.WHOIS_Lookup import controller as whois_controller
    from modules.hostname_resolver import (
        controller as hostname_resolver_controller,
    )
except ImportError as e:
    print(f"\n[Initialization Error] Failed to load module dependency: {e}")
    print("Please ensure all modules and required packages are installed.")
    sys.exit(1)


def display_menu():
    """Renders the main Network Toolkit menu options to the console."""
    print("\n==============================")
    print(" Network Toolkit")
    print("==============================")
    print("1.  Hostname Resolver")
    print("2.  Port Scanner")
    print("3.  Ping Host")
    print("4.  Local IP Information")
    print("5.  DNS Lookup")
    print("6.  Public IP Information")
    print("7.  IP Geolocation")
    print("8.  WHOIS Lookup")
    print("9.  Check Website Availability")
    print("10. HTTP Header Viewer")
    print("11. SSL Certificate Viewer")
    print("12. Reverse DNS Lookup")
    print("13. Traceroute")
    print("0.  Exit")


def get_menu_dispatch():
    """Maps menu option strings directly to their corresponding module controllers.

    Returns:
        dict: Mapping of string choice keys to function references.
    """
    return {
        "1": hostname_resolver_controller,
        "2": port_controller,
        "3": ping_controller,
        "4": ipinfo_controller,
        "5": dns_controller,
        "6": public_controller,
        "7": geo_controller,
        "8": whois_controller,
        "9": avail_controller,
        "10": header_controller,
        "11": ssl_controller,
        "12": reverse_dns_controller,
        "13": traceroute_controller,
    }


def main():
    """Master menu loop orchestrating execution of network toolkit modules."""
    dispatch = get_menu_dispatch()

    while True:
        try:
            display_menu()
            choice = input("\nEnter your choice (0-13): ").strip()

            if choice == "0":
                print("\nExiting Network Toolkit. Goodbye!")
                break

            if choice in dispatch:
                # Execute selected module controller cleanly
                dispatch[choice]()
            else:
                print("\nInvalid choice. Please enter a number between 0 and 13.")

        except RuntimeError as e:
            # Catch module network errors without crashing the main application loop
            print(f"\n[Tool Error] {e}")
            input("\nPress Enter to return to the main menu...")
        except KeyboardInterrupt:
            # Catch Ctrl+C during input or execution and return gracefully to main loop
            print("\n\nOperation cancelled by user.")


if __name__ == "__main__":
    main()