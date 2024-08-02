import unittest
from unittest.mock import patch, MagicMock
from baseprompt.client import Baseprompt
from baseprompt.config import Config


class TestBaseprompt(unittest.TestCase):
    def setUp(self):
        self.baseprompt_api_key = "test_baseprompt_api_key"
        self.openai_api_key = "test_openai_api_key"
        self.prompt_id = "test_prompt_id"
        self.prompt = "test_prompt"
        self.name = "test_name"
        self.client = Baseprompt(self.baseprompt_api_key)

    @patch("baseprompt.client.requests.request")
    def test_get_prompt(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "mocked_response"}
        mock_request.return_value = mock_response

        result = self.client.get_prompt(self.prompt_id)
        self.assertEqual(result, {"data": "mocked_response"})

        mock_request.assert_called_once_with(
            "POST",
            f"{Config.BASEPROMPT_BASE_URL}/get_prompt",
            headers=self.client._baseprompt_headers(),
            json={"api_key": self.baseprompt_api_key, "prompt_id": self.prompt_id}
        )

    @patch("baseprompt.client.requests.request")
    def test_create_prompt(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "mocked_response"}
        mock_request.return_value = mock_response

        result = self.client.create_prompt(self.prompt, name=self.name)
        self.assertEqual(result, {"data": "mocked_response"})

        mock_request.assert_called_once_with(
            "POST",
            f"{Config.BASEPROMPT_BASE_URL}/create_prompt",
            headers=self.client._baseprompt_headers(),
            json={
                "api_key": self.baseprompt_api_key,
                "prompt": self.prompt,
                "type": "personal",
                "model": "gpt-4o",
                "name": self.name,
                "output": None
            }
        )

    @patch("baseprompt.client.requests.request")
    def test_make_request_baseprompt(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "mocked_response"}
        mock_request.return_value = mock_response

        endpoint = "test_endpoint"
        result = self.client.make_request(endpoint, baseprompt=True)
        self.assertEqual(result, {"data": "mocked_response"})

        mock_request.assert_called_once_with(
            "GET",
            f"{Config.BASEPROMPT_BASE_URL}/{endpoint}",
            headers=self.client._baseprompt_headers(),
            json=None
        )

    def test_set_openai_api_key(self):
        new_api_key = "new_openai_api_key"
        self.client.set_openai_api_key(new_api_key)
        self.assertEqual(self.client.openai_api_key, new_api_key)

    def test_set_baseprompt_api_key(self):
        new_api_key = "new_baseprompt_api_key"
        self.client.set_baseprompt_api_key(new_api_key)
        self.assertEqual(self.client.baseprompt_api_key, new_api_key)

    def test_set_prompt_id(self):
        new_prompt_id = "new_prompt_id"
        self.client.set_prompt_id(new_prompt_id)
        self.assertEqual(self.client.prompt_id, new_prompt_id)


if __name__ == "__main__":
    unittest.main()
