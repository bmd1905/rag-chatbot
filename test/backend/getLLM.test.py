import unittest
from backend.chatbot.getLLM import GetLLM

class TestGetLLM(unittest.TestCase):
    
    def test_init_with_valid_api_key(self):
        llm_name = "test-llm"
        api_key = "test-api-key"
        llm = GetLLM(llm_name=llm_name, api_key=api_key)
        self.assertIsInstance(llm.Groqclient, Groq)
        self.assertEqual(llm.llm_name, llm_name)
        self.assertEqual(llm.Groqclient.api_key, api_key)


def test_init_sets_llm_name(self):
    llm_name = "test-model"
    api_key = "test-api-key"
    llm = GetLLM(llm_name=llm_name, api_key=api_key)
    self.assertEqual(llm.llm_name, llm_name)
def test_init_invalid_api_key(self):
    with self.assertRaises(ValueError):
        GetLLM(llm_name='test-model', api_key='invalid_key')

if __name__ == '__main__':
    unittest.main()
