import torch
from typing import List, Dict
import sys

class TransformersBackend:
    def __init__(self, model_id: str = "NCAIR1/N-ATLaS", hf_token: str = None, device: str = "cpu"):
        self.model_id = model_id
        self.device = "cuda" if device == "cuda" and torch.cuda.is_available() else "cpu"
        self.hf_token = hf_token
        
        try:
            from transformers import AutoModelForCausalLM, AutoTokenizer
        except ImportError:
            raise ImportError("Please install transformers and torch to use the TransformersBackend.")
            
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, token=hf_token)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, 
            token=hf_token, 
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None
        )
        if self.device == "cpu":
            self.model.to("cpu")

    def generate(self, messages: List[Dict[str, str]], stream: bool = False) -> str:
        prompt = self.tokenizer.apply_chat_template(
            messages, 
            tokenize=False, 
            add_generation_prompt=True
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=1000,
            temperature=0.1,
            repetition_penalty=1.12,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        generated_ids = outputs[0][inputs.input_ids.shape[-1]:]
        response = self.tokenizer.decode(generated_ids, skip_special_tokens=True)
        return response
