import urllib.request

def get_host():
    print("=" * 16)
    print("HTTP_Header_Viewer")
    print("=" * 16)
    web_name = input("Enter the host : ")
    return web_name


def host_validation(host_name):
    if host_name.lower().startswith(("https://", "http://")):
        return host_name
    else:
        host = "https://" + host_name
        return host


def get_header(host_name):
    try:
        header = urllib.request.urlopen(host_name)
        response = header.headers
        return response
    except urllib.error.URLError:
        return {
    "status": "fail",
    "reason": "DNS resolution failed."
}


def display(header):
    if header.get("status") == "fail":
        print("Connection faild")
    else:
        server = header.get("server")
        Content_Type = header.get("Content-Type")
        Content_Length = header.get("Content-Length")
        Date = header.get("Date")
        Connection = header.get("Connection")
        print(f"Server : '{server}'\n Content Type : '{Content_Type}'\n Content Length : '{Content_Length}'\n Data : '{Date}'\n Connection : '{Connection}'")


def controller():
    host = get_host()
    host_name = host_validation(host)
    header = get_header(host_name)
    display(header)