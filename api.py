import requests


class TaigaAPI:
    def __init__(self, token="", host="https://track.miem.hse.ru", token_type="Bearer"):
        self.__url = host + "/api/v1/"
        self.__token = token
        self.__token_type = token_type
        self.__params = {}
        self.__headers = {
            "Content-Type": "application/json",
            "Authorization": "{} {}".format(self.__token_type, token)
        }

    def get(self, obj="users", limit=False, number_of_entries=100):
        if limit:
            self.__params["page_size"] = str(number_of_entries)
        else:
            self.__headers["x-disable-pagination"] = "True"
        r = requests.get(self.__url + obj, params=self.__params, headers=self.__headers)
        try:
            r.raise_for_status()
            if 200 <= r.status_code < 300:
                return r.json()
        except requests.HTTPError as err:
            print(f"HTTP error occured: {err}")

    def auth(self, username, password):
        headers = {"Content-type": "application/json"}
        data = {"password": password, "type": "normal", "username": username}
        r = requests.post(self.__url + "auth", headers=headers, json=data)
        try:
            if r.status_code == 200:
                token = r.json()["auth_token"]
                self.__token = token
                self.__headers = {
                    "Content-Type": "application/json",
                    "Authorization": "{} {}".format(self.__token_type, token)
                }
        except requests.HTTPError as err:
            print(f"Couldn't authorize. HTTP error occured: {err}")
