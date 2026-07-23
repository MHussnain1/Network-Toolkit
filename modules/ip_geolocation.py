import json
import urllib
from modules.public_ip import is_connected, public_ip


def geolocation_ip(ip):
    url = "http://ip-api.com/json/" + ip
    response = urllib.request.urlopen(url, timeout=5)
    data = response.read().decode()
    result = json.loads(data)
    return result


def display(ip, result):
    print("\n---------------------------")
    print("\n==============================")
    print("            Results")
    print("==============================")

    if result.get("status") == "success":
        print(f"""
        Status   : {result.get("status")}
        IP       : {ip}
        Country  : {result.get("country")}
        Region   : {result.get("regionName")}
        City     : {result.get("city")}
        Timezone : {result.get("timezone")}
        """)
    else:
        print("Status : fail")


def controller():
    if is_connected():
        ip = public_ip()
        result = geolocation_ip(ip)
        display(ip, result)

    else:
        print("Internet connection is unavailable")
