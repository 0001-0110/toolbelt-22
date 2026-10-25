import json
import sys
import requests
from os import getenv

mod_portal_url = "https://mods.factorio.com"
init_upload_url = f"{mod_portal_url}/api/v2/mods/releases/init_upload"
details_url = f"{mod_portal_url}/api/v2/mods/edit_details"


class UnknownModException(Exception):
    pass


def get_mod_name():
    with open("info.json") as info_file:
        return json.load(info_file)["name"]


def get_api_key():
    return getenv("MOD_PORTAL_API_KEY")


def get_headers():
    api_key = get_api_key()
    if (api_key is None):
        raise Exception("Missing API key")
    return {"Authorization": f"Bearer {api_key}"}


def finish_upload(file_path, init_response):
    upload_url = init_response.json()["upload_url"]
    with open(file_path, "rb") as file:
        request_body = {"file": file}
        response = requests.post(upload_url, files=request_body)
        if not response.ok:
            raise Exception(f"upload failed: {response.text}")


def update_mod(file_path):
    mod_name = get_mod_name()
    request_body = {"mod": mod_name}
    request_headers = get_headers()
    response = requests.post(init_upload_url, data=request_body, headers=request_headers)
    if not response.ok:
        match response.json()["error"]:
            case "UnknownMod":
                raise UnknownModException()
            case _:
                raise Exception(f"init_upload failed: {response.text}")
    finish_upload(file_path, response)
    print(f"update successful: {response.text}")


def publish_mod(file_path):
    mod_name = get_mod_name()
    request_headers = get_headers()
    with open("README.md", "rb") as file:
        request_body = {"mod": mod_name, "description": file.read()}
    response = requests.post(details_url, data=request_body, headers=request_headers)
    if not response.ok:
        raise Exception(f"init_publish failed: {response.text}")
    finish_upload(file_path)
    print(f"publish successful: {response.text}")


def upload():
    file_path = sys.argv[1]

    try:
        update_mod(file_path)
    except UnknownModException:
        publish_mod(file_path)


if __name__ == "__main__":
    upload()
