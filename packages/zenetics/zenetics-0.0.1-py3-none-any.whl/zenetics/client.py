from typing import Dict

import requests


class APIClientError(Exception):
    pass


class APIClient:
    def __init__(self, address: str):
        self.address = address

    def post(self, body: Dict, api_key: str):
        headers = {
            "Content-Type": "application/json",
            "ZENETICS_API_KEY": api_key,
        }

        response = requests.post(
            self.address + "/api/v1/sessions", json=body, headers=headers
        )
        if response.status_code != 200:
            raise APIClientError(f"Failed to post to {self.address}")
