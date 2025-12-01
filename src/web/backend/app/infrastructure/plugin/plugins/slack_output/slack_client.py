"""Slack API client."""
import aiohttp
from typing import Optional, Dict, Any


class SlackClient:
    """Client for sending messages to Slack via webhook."""
    
    def __init__(self, webhook_url: str):
        """Initialize Slack client.
        
        Args:
            webhook_url: Slack webhook URL
        """
        self.webhook_url = webhook_url
    
    async def send_message(
        self,
        text: str,
        channel: Optional[str] = None,
        username: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Send a message to Slack.
        
        Args:
            text: Message text
            channel: Optional channel name
            username: Optional bot username
            
        Returns:
            Response dictionary
        """
        payload = {
            "text": text,
        }
        
        if channel:
            payload["channel"] = channel
        
        if username:
            payload["username"] = username
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.webhook_url, json=payload) as response:
                response_text = await response.text()
                
                if response.status == 200:
                    return {
                        "status": "ok",
                        "response": response_text,
                    }
                else:
                    return {
                        "status": "error",
                        "status_code": response.status,
                        "response": response_text,
                    }

