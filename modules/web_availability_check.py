import urllib.request


def get_website():
    print("=" * 16)
    print("Web availability checker")
    print("=" * 16)
    web_name = input("Enter the website : ")
    return web_name


def validate_webName(web_name):
    if web_name.lower().startswith(("https://", "http://")):
        return web_name
    else:
        web_name = "https://" + web_name
        return web_name


def check_website(url):
    try:
        response = urllib.request.urlopen(url)
        return {
            "status": "success",
            "status_code": response.getcode(),
            "reason": response.reason,
            "final_url": response.geturl(),
        }
    except urllib.error.URLError as error:
        return {"status": "fail", "reason": str(error)}


# for debug print(response)
# print(type(response))
# print(dir(response))
# print(response.status)
# print(response.reason)
# print(response.getcode())
# print(response.geturl())


def display(result):

    if result.get("status") == "success":
        status_code = result.get("status_code")
        reason = result.get("reason")
        final_url = result.get("final_url")
        print(
            f" status : success \n status code : '{status_code}'\n reason : '{reason}'\n final url : '{final_url}'"
        )
    else:
        status = result.get("status")
        print(f" status : '{status}'\n reason : DNS resolution failed.'")


def controller():
    web_name = get_website()
    url = validate_webName(web_name)
    result = check_website(url)
    display(result)
