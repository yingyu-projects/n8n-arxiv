"""LLM client for summarization."""
import requests
import json
from typing import Dict, Any
from abc import ABC, abstractmethod

from app.infrastructure.services.config_loader import ConfigLoader


class LLMClient(ABC):
    """Abstract LLM client interface."""
    
    @abstractmethod
    def summarize(self, prompt: str, text: str, paper_link: str) -> Dict[str, Any]:
        """Summarize paper text."""
        pass


class LocalLLMClient(LLMClient):
    """Local LLM client (OpenAI-compatible API)."""
    
    def __init__(self, base_url: str, model: str, endpoint: str = "/v1/responses"):
        """Initialize local LLM client."""
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.endpoint = endpoint
        self.timeout = 3600  # 1 hour timeout
    
    def summarize(self, prompt: str, text: str, paper_link: str) -> Dict[str, Any]:
        """Summarize paper using local LLM."""
        url = f"{self.base_url}{self.endpoint}"
        
        full_prompt = f"{prompt}\n{text}\n paper_link: {paper_link}"
        
        payload = {
            "input": [
                {
                    "type": "message",
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "model": self.model,
            "stream": False,
            "text": {}
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()
            
            result = response.json()
            
            # Extract content from response
            if "output" in result and len(result["output"]) > 0:
                content = result["output"][0].get("content", [])
                if len(content) > 0:
                    text_content = content[0].get("text", "")
                    # Try to parse as JSON
                    try:
                        # Clean JSON string
                        cleaned = text_content.strip()
                        # Remove markdown code blocks if present
                        if cleaned.startswith("```json"):
                            cleaned = cleaned[7:]
                        if cleaned.startswith("```"):
                            cleaned = cleaned[3:]
                        if cleaned.endswith("```"):
                            cleaned = cleaned[:-3]
                        cleaned = cleaned.strip()
                        
                        return json.loads(cleaned)
                    except json.JSONDecodeError:
                        # If not JSON, return as text
                        return {"content": text_content}
            
            raise Exception("Invalid response format from LLM")
            
        except requests.RequestException as e:
            raise Exception(f"Failed to call LLM: {str(e)}")


class OpenAILLMClient(LLMClient):
    """OpenAI API client."""
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """Initialize OpenAI client."""
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def summarize(self, prompt: str, text: str, paper_link: str) -> Dict[str, Any]:
        """Summarize paper using OpenAI API."""
        full_prompt = f"{prompt}\n{text}\n paper_link: {paper_link}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",
                    "content": full_prompt
                }
            ],
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=300
            )
            response.raise_for_status()
            
            result = response.json()
            content = result["choices"][0]["message"]["content"]
            
            # Try to parse as JSON
            try:
                cleaned = content.strip()
                if cleaned.startswith("```json"):
                    cleaned = cleaned[7:]
                if cleaned.startswith("```"):
                    cleaned = cleaned[3:]
                if cleaned.endswith("```"):
                    cleaned = cleaned[:-3]
                cleaned = cleaned.strip()
                
                return json.loads(cleaned)
            except json.JSONDecodeError:
                return {"content": content}
                
        except requests.RequestException as e:
            raise Exception(f"Failed to call OpenAI: {str(e)}")


def create_llm_client(config_loader: ConfigLoader) -> LLMClient:
    """Factory function to create appropriate LLM client."""
    config = config_loader.load_config()
    provider = config.get("llm", {}).get("provider", "local")
    
    if provider == "openai":
        openai_config = config.get("llm", {}).get("openai", {})
        return OpenAILLMClient(
            api_key=openai_config.get("api_key", ""),
            model=openai_config.get("model", "gpt-4")
        )
    else:
        local_config = config.get("llm", {}).get("local", {})
        return LocalLLMClient(
            base_url=local_config.get("base_url", "http://127.0.0.1:1234"),
            model=local_config.get("model", "qwen/qwen3-vl-8b"),
            endpoint=local_config.get("endpoint", "/v1/responses")
        )

