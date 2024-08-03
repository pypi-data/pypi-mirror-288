import requests
from .config import Config

class Baseprompt:
    def __init__(self, baseprompt_api_key):
        self.baseprompt_api_key = baseprompt_api_key
        self.base_url = Config.API_BASE_URL

    def _baseprompt_headers(self):
        return {
            "Content-Type": "application/json",
            "apiKey": f"{self.baseprompt_api_key}"
        }

    def set_baseprompt_api_key(self, api_key):
        """Setter for the Baseprompt API key"""
        if not api_key:
            raise ValueError("An API key cannot be empty")
        self.baseprompt_api_key = api_key

    def make_request(self, endpoint, method="GET", data=None):
        headers = self._baseprompt_headers()
        url = f"{self.base_url}/{endpoint}"

        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def run_workflow(self, workflow_id, messages=None):
        payload = {
            'workflowId': workflow_id,
        }

        if messages:
            payload['messages'] = messages

        response = self.make_request(endpoint='run_workflow', method="POST", data=payload)
        return response
