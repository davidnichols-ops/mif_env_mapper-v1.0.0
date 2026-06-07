"""
Data Sanitizer Module
Enforces data minimization by masking sensitive data types.
"""

import re
from typing import Any, Union
from .config import SENSITIVE_PATTERNS


class DataSanitizer:
    """
    Enforces strict data minimization boundaries by masking sensitive data types.
    
    Methods:
        sanitize_string(text): Applies sanitization regex to raw strings
        sanitize_structure(data): Recursively scrubs all string content in structures
    """
    
    def __init__(self, additional_patterns: list = None):
        """
        Initialize with default patterns plus any additional custom patterns.
        
        Args:
            additional_patterns: Optional list of (compiled_regex, replacement) tuples
        """
        self.sensitive_patterns = list(SENSITIVE_PATTERNS)
        if additional_patterns:
            self.sensitive_patterns.extend(additional_patterns)
    
    def sanitize_string(self, text: str) -> str:
        """
        Applies sanitization regex patterns sequentially to raw input strings.
        
        Args:
            text: Raw string to sanitize
            
        Returns:
            Sanitized string with sensitive data replaced
        """
        if not isinstance(text, str):
            return text
        
        clean_text = text
        for pattern, replacement in self.sensitive_patterns:
            clean_text = pattern.sub(replacement, clean_text)
        return clean_text
    
    def sanitize_structure(self, data: Any) -> Any:
        """
        Recursively parses data structures to scrub all string content.
        
        Args:
            data: Any data structure (dict, list, str, or primitive)
            
        Returns:
            Sanitized copy of the data structure
        """
        if isinstance(data, dict):
            return {k: self.sanitize_structure(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_structure(item) for item in data]
        elif isinstance(data, str):
            return self.sanitize_string(data)
        else:
            # Return primitives (int, float, bool, None) as-is
            return data
    
    def add_pattern(self, pattern: str, replacement: str, flags: int = 0) -> None:
        """
        Add a custom sanitization pattern at runtime.
        
        Args:
            pattern: Regex pattern string
            replacement: Replacement string
            flags: Optional regex flags
        """
        compiled = re.compile(pattern, flags)
        self.sensitive_patterns.append((compiled, replacement))
    
    def get_pattern_count(self) -> int:
        """Return the number of active sanitization patterns."""
        return len(self.sensitive_patterns)
