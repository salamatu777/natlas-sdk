import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from natlas.asr import ASRPipeline, ASRResult

class TestASRPipeline(unittest.TestCase):
    def test_asr_pipeline_models_dict(self):
        self.assertIn("ha", ASRPipeline.MODELS)
        self.assertIn("yo", ASRPipeline.MODELS)
        self.assertIn("ig", ASRPipeline.MODELS)
        self.assertIn("en", ASRPipeline.MODELS)
        self.assertEqual(ASRPipeline.MODELS["ha"], "NCAIR1/Hausa-ASR")
        self.assertEqual(ASRPipeline.MODELS["yo"], "NCAIR1/Yoruba-ASR")
        self.assertEqual(ASRPipeline.MODELS["ig"], "NCAIR1/Igbo-ASR")
        self.assertEqual(ASRPipeline.MODELS["en"], "NCAIR1/NigerianAccentedEnglish")

    def test_asr_pipeline_device(self):
        pipeline = ASRPipeline(device="cpu")
        self.assertEqual(pipeline.device, "cpu")

if __name__ == '__main__':
    unittest.main()
