"""Text cleaning service."""
import re
from typing import Optional


class TextCleaner:
    """Service for cleaning academic paper text."""
    
    # Patterns to identify reference sections
    REF_PATTERNS = [
        re.compile(r'^references$', re.IGNORECASE | re.MULTILINE),
        re.compile(r'^bibliography$', re.IGNORECASE | re.MULTILINE),
        re.compile(r'^参考文献$', re.MULTILINE),
        re.compile(r'^acknowledgement', re.IGNORECASE | re.MULTILINE),
        re.compile(r'^acknowledgments', re.IGNORECASE | re.MULTILINE),
        re.compile(r'^致谢$', re.MULTILINE),
        re.compile(r'^appendix', re.IGNORECASE | re.MULTILINE),
        re.compile(r'^supplementary material', re.IGNORECASE | re.MULTILINE),
        re.compile(r'^ethics statement', re.IGNORECASE | re.MULTILINE),
    ]
    
    def clean(self, raw_text: str) -> str:
        """Clean paper text by removing references and non-essential content."""
        if not raw_text or not isinstance(raw_text, str):
            return ""
        
        text = raw_text
        
        # Remove reference section and everything after
        for pattern in self.REF_PATTERNS:
            match = pattern.search(text)
            if match:
                idx = match.start()
                text = text[:idx].strip()
                break
        
        return text
    
    def get_cleaning_stats(self, raw_text: str, cleaned_text: str) -> dict:
        """Get statistics about text cleaning."""
        original_length = len(raw_text) if raw_text else 0
        cleaned_length = len(cleaned_text) if cleaned_text else 0
        
        reduction_ratio = 0.0
        if original_length > 0:
            reduction_ratio = ((1 - cleaned_length / original_length) * 100)
        
        return {
            "original_length": original_length,
            "cleaned_length": cleaned_length,
            "reduction_ratio": f"{reduction_ratio:.1f}%"
        }

