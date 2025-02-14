import unittest
from get_llm import LLMClient
from groq import Groq
import dotenv
import os
from unittest import mock

# Ensure the script can find the .env file anywhere
dotenv.load_dotenv(dotenv.find_dotenv())


class TestLLMClient(unittest.TestCase):
    def setUp(self):
        self.llm_name = "llama-3.1-8b-instant"
        self.api_key = os.getenv("GROQ_KEY")
        self.llm_client = LLMClient(llm_name=self.llm_name, api_key=self.api_key)

    def test_initialize_llm_client_with_valid_params(self):
        llm_name = "test-model"
        api_key = "test-api-key"
        llm_client = LLMClient(llm_name=llm_name, api_key=api_key)

        self.assertEqual(llm_client.llm_name, llm_name)
        self.assertIsInstance(llm_client.groq_client, Groq)
        self.assertEqual(llm_client.groq_client.api_key, api_key)

    def test_generate_content_api_failure(self):
        self.llm_client.groq_client.chat.completions.create = mock.Mock(side_effect=Exception("API Error"))

        prompt_structure = [{"role": "user", "content": "Test prompt"}]

        result = self.llm_client.generate_content(prompt_structure)

        self.assertTrue(result.startswith("Error generating response:"))
        self.assertIn("API Error", result)

    def test_handle_invalid_llm_name(self):
        invalid_llm_name = "invalid-model"
        api_key = os.getenv("GROQ_KEY")
        llm_client = LLMClient(llm_name=invalid_llm_name, api_key=api_key)

        prompt_structure = [{"role": "user", "content": "Test message"}]

        response = llm_client.generate_content(prompt_structure)

        self.assertTrue(response.startswith("Error generating response:"))
        self.assertIn("invalid-model", response)


if __name__ == "__main__":
    unittest.main()
