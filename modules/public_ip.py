import socket
import urllib.request
import json


def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:                                    
        return False


def public_ip():
    response = urllib.request.urlopen(
        "https://api.ipify.org?format=json",
        timeout=5
    )

    data = response.read().decode()
    result = json.loads(data)

    return result["ip"]


def display(result):
    print("\n---------------------------")
    print("\n==============================")
    print("Results")
    print("==============================")

    print(f"\nThe public IP is: {result}")


def controller():
    if is_connected():
        result = public_ip()
        display(result)
    else:
        print("Internet connection is unavailable")