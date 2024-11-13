import json
import subprocess


class PATIssuer:
    def __init__(self, subscription: str):
        self.subscription = subscription

    def issue(self) -> str:
        raw_token_output = subprocess.check_output(
            ["az", "account", "get-access-token", "--subscription", self.subscription]
        )
        access_token = json.loads(raw_token_output)["accessToken"]
        return access_token
