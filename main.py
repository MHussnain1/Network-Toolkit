from modules.hostname_resolver import hostname_resolver
from modules.port_scanner import port_scanner
from modules.ping_host import controller
from modules.local_ipinformation import local_ip_information
from modules.DNS_Lookup import controller


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
        print("6. Exit")

        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == '1':
            hostname_resolver()

        elif choice == '2':
            port_scanner()

        elif choice == '3':
            controller()

        elif choice == '4':
            local_ip_information()

        elif choice == '5':
            controller()

        elif choice == '6':
            print("\nExiting the program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()