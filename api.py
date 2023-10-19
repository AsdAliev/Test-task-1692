import requests


class TaigaAPI:
    def __init__(self, token, host="https://track.miem.hse.ru", token_type="Bearer"):
        self.url = host + "/api/v1/"
        self.params = {}
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "{} {}".format(token_type, token)
        }

    def get(self, obj="users", pagination=False, page=1, page_size=100):
        if pagination:
            self.params["page"] = str(page)
            self.params["page_size"] = str(page_size)
        else:
            self.headers["x-disable-pagination"] = "True"
        r = requests.get(self.url + obj, params=self.params, headers=self.headers)
        try:
            r.raise_for_status()
            if 200 <= r.status_code < 300:
                return r.json()
        except requests.HTTPError as err:
            print(f"HTTP error occured: {err}")
