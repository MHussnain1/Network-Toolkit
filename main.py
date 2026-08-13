import sys


# ============================================================
# Module Imports
# ============================================================

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
    print("\n==============================")
    print(" Initialization Error")
    print("==============================")
    print(f"\nFailed to load a Network Toolkit module:")
    print(f"{e}")
    print("\nPlease check that:")
    print("  - All module files exist.")
    print("  - Module filenames are correct.")
    print("  - Required packages are installed.")
    print("  - You are running the program from the project root.")
    sys.exit(1)


# ============================================================
# User Interface
# ============================================================

def display_menu():
    """Display the main Network Toolkit menu."""

    print("\n==============================")
    print("      Network Toolkit")
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


def pause():
    """Pause execution before returning to the main menu."""

    try:
        input("\nPress Enter to return to the main menu...")
    except KeyboardInterrupt:
        print("\n\nReturning to main menu...")


# ============================================================
# Menu Dispatch
# ============================================================

def get_menu_dispatch():
    """
    Return a mapping between menu choices and module controllers.

    Returns:
        dict: Menu option mapped to its corresponding controller.
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


# ============================================================
# Main Application
# ============================================================

def main():
    """Run the main Network Toolkit application loop."""

    dispatch = get_menu_dispatch()

    while True:
        try:
            display_menu()

            choice = input("\nEnter your choice (0-13): ").strip()

            # ------------------------------------------------
            # Exit
            # ------------------------------------------------

            if choice == "0":
                print("\nExiting Network Toolkit. Goodbye!")
                break

            # ------------------------------------------------
            # Execute selected module
            # ------------------------------------------------

            if choice in dispatch:
                print()

                controller = dispatch[choice]
                controller()

                pause()

            # ------------------------------------------------
            # Invalid choice
            # ------------------------------------------------

            else:
                print(
                    "\nInvalid choice."
                    "\nPlease enter a number between 0 and 13."
                )

        except KeyboardInterrupt:
            print("\n\nOperation cancelled.")

            try:
                continue_running = input(
                    "\nPress Enter to return to the menu "
                    "or type '0' to exit: "
                ).strip()

                if continue_running == "0":
                    print("\nExiting Network Toolkit. Goodbye!")
                    break

            except KeyboardInterrupt:
                print("\n\nExiting Network Toolkit. Goodbye!")
                break

        except RuntimeError as e:
            print("\n==============================")
            print(" Tool Error")
            print("==============================")
            print(f"\n{e}")

            pause()

        except Exception as e:
            # Last-resort protection so one unexpected module
            # error does not terminate the entire toolkit.
            print("\n==============================")
            print(" Unexpected Error")
            print("==============================")
            print(f"\n{type(e).__name__}: {e}")

            pause()


# ============================================================
# Script Entry Point
# ============================================================

if __name__ == "__main__":
    main()