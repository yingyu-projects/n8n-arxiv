"""Slack output plugin."""
import json
from typing import Dict, Any, Optional

from app.domain.paper.entities.paper import Paper
from app.domain.plugin.value_objects.config_schema import ConfigSchema
from app.infrastructure.plugin.base_plugin import OutputPlugin
from app.application.plugin.core_api import CoreAPI


class SlackOutputPlugin(OutputPlugin):
    """Slack output plugin for sending parsed papers to Slack."""
    
    def __init__(self, core_api: Optional[CoreAPI] = None):
        """Initialize Slack output plugin."""
        super().__init__(
            name="slack_output",
            version="1.0.0",
            metadata={
                "description": "Send parsed papers to a Slack channel via webhook",
                "author": "arXiv Parser",
            },
            core_api=core_api
        )
    
    def get_config_schema(self) -> ConfigSchema:
        """Get plugin configuration schema."""
        schema = {
            "type": "object",
            "properties": {
                "webhook_url": {
                    "type": "string",
                    "title": "Webhook URL",
                    "description": "Slack webhook URL for posting messages",
                },
                "channel": {
                    "type": "string",
                    "title": "Channel",
                    "description": "Slack channel name (optional, can be set in webhook)",
                    "default": "",
                },
                "username": {
                    "type": "string",
                    "title": "Username",
                    "description": "Bot username for Slack messages",
                    "default": "arXiv Bot",
                },
            },
            "required": ["webhook_url"],
        }
        return ConfigSchema.from_dict(schema)
    
    async def execute(self, paper: Paper, config: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the plugin to send paper to Slack.
        
        Args:
            paper: The parsed paper entity
            config: Plugin configuration values
            
        Returns:
            Dict containing execution result
        """
        webhook_url = config.get("webhook_url")
        if not webhook_url:
            raise ValueError("webhook_url is required")
        
        channel = config.get("channel", "")
        username = config.get("username", "arXiv Bot")
        
        # Format message
        message = self._format_message(paper)
        
        # Use CoreAPI for HTTP requests and logging
        self.api.log_info(f"Sending paper {paper.id} to Slack", self.name)
        
        try:
            # Prepare Slack webhook payload
            payload = {
                "text": message,
            }
            
            if channel:
                payload["channel"] = channel
            
            if username:
                payload["username"] = username
            
            # Use CoreAPI HTTP client
            response = await self.api.http_post(
                url=webhook_url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response['status'] == 200:
                self.api.log_info("Paper sent to Slack successfully", self.name)
                return {
                    "success": True,
                    "message": "Paper sent to Slack successfully",
                    "slack_response": response['body'],
                }
            else:
                error_msg = f"Slack API returned status {response['status']}"
                self.api.log_error(error_msg, self.name)
                raise ValueError(error_msg)
        
        except Exception as e:
            self.api.log_error("Failed to send to Slack", self.name, e)
            raise
    
    def _format_message(self, paper: Paper) -> str:
        """Format paper information as Slack message.
        
        Args:
            paper: Paper entity
            
        Returns:
            Formatted message string
        """
        lines = [
            f"*{paper.title}*",
            f"Category: {paper.category}",
        ]
        
        if paper.arxiv_id:
            lines.append(f"ArXiv ID: {paper.arxiv_id}")
        
        lines.append(f"PDF: {paper.get_pdf_link_str()}")
        
        if paper.summary:
            summary_dict = paper.summary.to_dict()
            if isinstance(summary_dict, dict):
                topic = summary_dict.get("topic", "")
                if topic:
                    lines.append(f"\n*Summary:*\n{topic}")
        
        return "\n".join(lines)

