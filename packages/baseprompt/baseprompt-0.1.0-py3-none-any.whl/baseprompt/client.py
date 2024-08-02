import requests
from .config import Config


class Baseprompt:
    def __init__(self, baseprompt_api_key):
        self.baseprompt_api_key = baseprompt_api_key
        self.base_url = Config.API_BASE_URL

    def _baseprompt_headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.baseprompt_api_key}"
        }

    def set_baseprompt_api_key(self, api_key):
        """Setter for the Baseprompt API key"""
        if not api_key:
            raise ValueError("An API key cannot be empty")
        self.baseprompt_api_key = api_key

    def make_request(self, endpoint, method="GET", data=None):
        if not self.baseprompt_api_key:
            raise ValueError("A Baseprompt API key is required for making requests")
        url = f"{Config.BASEPROMPT_BASE_URL}/{endpoint}"
        headers = self._baseprompt_headers()

        response = requests.request(method, url, headers=headers, json=data)
        response.raise_for_status()
        return response.json()

    def get_prompt(self, prompt_id):
        endpoint = "get_prompt"

        if not self.baseprompt_api_key:
            raise ValueError("a baseprompt api key is required for making requests")
        if not prompt_id:
            raise ValueError("a sprompt id is required for making requests")

        data = {
            "api_key": self.baseprompt_api_key,
            "prompt_id": prompt_id
        }

        response = self.make_request(endpoint=endpoint, method="POST", data=data)
        return response

    def run_workflow(self, workflow_id, entry_data=None):
        payload = {
            'workflowId': workflow_id,
            'apiKey': self.baseprompt_api_key
        }

        if entry_data:
            payload['entryData'] = entry_data

        response = self.make_request(endpoint='run_workflow', method="POST", data=payload)
        return response

        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     response.raise_for_status()

