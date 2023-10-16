import requests
import json
import os
from dotenv import load_dotenv


class Request:
    def __init__(self, token, host="https://track.miem.hse.ru", token_type="Bearer"):
        self.url = host + "/api/v1/users"
        self.params = {
            "page": "2",
            "page_size": "100",
        }
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "{} {}".format(token_type, token)
        }

    def get(self, pagination=True):
        if not pagination:
            self.headers["x-disable-pagination"] = "True"

        r = requests.get(self.url, params=self.params, headers=self.headers)

        print(len(r.json()))

        if 200 <= r.status_code < 300:
            with open("info.json", "w", encoding="utf-8") as f:
                json.dump(r.json(), f, indent=2, ensure_ascii=False)
        else:
            print(r.status_code)


if __name__ == "__main__":
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
        TOKEN = os.environ.get('TOKEN')
    else:
        exit(1)

    req = Request(TOKEN)
    req.get()
