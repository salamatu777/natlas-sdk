import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from natlas.chat import ChatPipeline, ChatResponse, ChatMessage

class TestChatPipeline(unittest.TestCase):
    def test_chat_pipeline_init(self):
        pipeline = ChatPipeline(backend="ollama")
        self.assertEqual(pipeline.backend_type, "ollama")
        self.assertGreaterEqual(len(pipeline.history), 1)
        self.assertEqual(pipeline.history[0]["role"], "system")
        self.assertIn("Awarri", pipeline.history[0]["content"])

    def test_chat_pipeline_generate(self):
        pipeline = ChatPipeline(backend="ollama")
        pipeline.backend.generate = MagicMock(return_value="Bawo ni o se wa?")
        
        response = pipeline.generate("Bawo ni?", language="yo")
        self.assertIsInstance(response, ChatResponse)
        self.assertEqual(response.text, "Bawo ni o se wa?")
        self.assertEqual(response.language, "yo")
        # Check history updated
        self.assertEqual(pipeline.history[-1]["role"], "assistant")
        self.assertEqual(pipeline.history[-1]["content"], "Bawo ni o se wa?")

if __name__ == '__main__':
    unittest.main()
