"""Paper parsing domain service."""
from typing import List
from app.domain.paper.entities.paper import Paper
from app.domain.paper.value_objects.summary import Summary


class PaperParsingService:
    """Domain service for paper parsing business logic."""
    
    def validate_paper_for_parsing(self, paper: Paper) -> bool:
        """Validate if paper can be parsed."""
        if paper.is_parsed():
            return False
        return True
    
    def prepare_paper_for_summary(self, paper: Paper, cleaned_text: str) -> str:
        """Prepare paper content for summarization."""
        # This could include additional domain logic for preparing text
        return cleaned_text

