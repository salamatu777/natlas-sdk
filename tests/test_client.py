import unittest
from unittest.mock import MagicMock
import os
import sys

# Ensure SDK root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from natlas import NAtlasClient

class TestNAtlasClient(unittest.TestCase):
    def test_client_initialization_defaults(self):
        client = NAtlasClient(backend="ollama")
        self.assertEqual(client.backend_type, "ollama")
        self.assertIsNotNone(client.chat_pipeline)

    def test_client_chat_mock(self):
        client = NAtlasClient(backend="ollama")
        mock_resp = MagicMock()
        mock_resp.text = "Sannu, yaya kake?"
        mock_resp.language = "ha"
        client.chat_pipeline.generate = MagicMock(return_value=mock_resp)
        
        res = client.chat("Sannu", language="ha")
        self.assertEqual(res.text, "Sannu, yaya kake?")
        self.assertEqual(res.language, "ha")

    def test_client_backend_selection(self):
        client_openai = NAtlasClient(backend="ollama", ollama_model="natlas")
        self.assertEqual(client_openai.backend_type, "ollama")

if __name__ == '__main__':
    unittest.main()
