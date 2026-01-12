"""SiliconFlow API client"""
import os
import json
import base64
from typing import List, Dict, Optional
import requests
from bilivagent.config import Config


class SiliconFlowClient:
    """Client for SiliconFlow API"""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or Config.SILICONFLOW_API_KEY
        self.base_url = base_url or Config.SILICONFLOW_BASE_URL
        
        if not self.api_key:
            raise ValueError("API key is required")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def chat_completion(self, messages: List[Dict], model: Optional[str] = None, temperature: float = 0.7, max_tokens: int = 2000) -> str:
        """Call chat completion API"""
        model = model or Config.LLM_MODEL
        
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"Error calling chat completion API: {e}")
            return ""
    
    def _encode_image(self, image_path: str) -> tuple:
        """Encode image to base64 and return with mime type"""
        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode('utf-8')

        # Determine image type from extension
        ext = image_path.lower().split('.')[-1]
        mime_type = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp'
        }.get(ext, 'image/jpeg')

        return image_data, mime_type

    def vision_analysis(self, image_path: str, prompt: str, model: Optional[str] = None) -> str:
        """Analyze single image using vision model"""
        return self.vision_analysis_multi([image_path], prompt, model)

    def vision_analysis_multi(self, image_paths: List[str], prompt: str, model: Optional[str] = None) -> str:
        """
        Analyze multiple images using vision model.
        Based on SiliconFlow multimodal vision API documentation.
        """
        model = model or Config.VLM_MODEL
        
        if not image_paths:
            return ""

        # Build content with multiple images
        content = []

        # Add all images first
        for image_path in image_paths:
            if not os.path.exists(image_path):
                Config.debug_print(f"[DEBUG] Image not found: {image_path}")
                continue

            image_data, mime_type = self._encode_image(image_path)
            content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{image_data}"
                }
            })

        # Add text prompt at the end
        content.append({
            "type": "text",
            "text": prompt
        })

        if len(content) <= 1:  # Only text, no valid images
            return ""

        messages = [
            {
                "role": "user",
                "content": content
            }
        ]
        
        url = f"{self.base_url}/chat/completions"
        
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": 2000,
            "temperature": 0.7
        }

        Config.debug_print(f"[DEBUG] Analyzing {len(image_paths)} images with model: {model}")

        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=180)

            # Check for errors and print detailed info
            if response.status_code != 200:
                print(f"Vision API error: {response.status_code}")
                Config.debug_print(f"[DEBUG] Response: {response.text}")
                # Try to parse error message
                try:
                    error_data = response.json()
                    error_msg = error_data.get('error', {}).get('message', response.text)
                    Config.debug_print(f"[DEBUG] Error message: {error_msg}")
                except:
                    pass
                return ""

            result = response.json()
            Config.debug_print(f"[DEBUG] Vision API response received")
            return result["choices"][0]["message"]["content"]
        except requests.exceptions.Timeout:
            print("Vision API timeout (180s)")
            return ""
        except Exception as e:
            print(f"Error calling vision API: {e}")
            if Config.DEBUG:
                import traceback
                traceback.print_exc()
            return ""
