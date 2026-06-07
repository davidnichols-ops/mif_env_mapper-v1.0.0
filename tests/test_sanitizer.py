"""
Tests for DataSanitizer module.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mif_env_mapper.sanitizer import DataSanitizer


class TestDataSanitizer(unittest.TestCase):
    """Test cases for DataSanitizer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.sanitizer = DataSanitizer()
    
    # ---- PII Path Tests ----
    
    def test_redacts_macos_user_paths(self):
        """Verify /Users/ paths are masked."""
        input_str = "/Users/johndoe/projects/app/config"
        result = self.sanitizer.sanitize_string(input_str)
        self.assertNotIn("johndoe", result)
        self.assertIn("[REDACTED_USER]", result)
    
    def test_redacts_linux_home_paths(self):
        """Verify /home/ paths are masked."""
        input_str = "/home/janedoe/.ssh/id_rsa"
        result = self.sanitizer.sanitize_string(input_str)
        self.assertNotIn("janedoe", result)
        self.assertIn("[REDACTED_USER]", result)
    
    # ---- Credential Tests ----
    
    def test_redacts_passwords_in_strings(self):
        """Verify password= values are masked."""
        input_str = "mysql://root:supersecret123@localhost:3306/db"
        result = self.sanitizer.sanitize_string(input_str)
        self.assertNotIn("supersecret123", result)
        self.assertIn("[REDACTED]", result)
    
    def test_redacts_auth_tokens(self):
        """Verify auth_token= values are masked."""
        input_str = "auth_token=ghp_ABC123DEF456GHI789"
        result = self.sanitizer.sanitize_string(input_str)
        self.assertNotIn("ghp_ABC123DEF456GHI789", result)
    
    def test_redacts_api_keys(self):
        """Verify api_key= values are masked."""
        input_str = "api_key=sk_live_1234567890abcdef"
        result = self.sanitizer.sanitize_string(input_str)
        self.assertNotIn("sk_live_1234567890abcdef", result)
    
    # ---- Network Tests ----
    
    def test_redacts_ip_addresses(self):
        """Verify IPv4 addresses are masked."""
        input_str = "Server at 192.168.1.100 responding"
        result = self.sanitizer.sanitize_string(input_str)
        self.assertNotIn("192.168.1.100", result)
        self.assertIn("[REDACTED_IP]", result)
    
    def test_redacts_email_addresses(self):
        """Verify email addresses are masked."""
        input_str = "Contact admin@example.com for access"
        result = self.sanitizer.sanitize_string(input_str)
        self.assertNotIn("admin@example.com", result)
        self.assertIn("[REDACTED_EMAIL]", result)
    
    # ---- Structure Tests ----
    
    def test_sanitize_nested_dict(self):
        """Verify recursive dict sanitization."""
        dirty = {
            "user": "/Users/devops/config",
            "nested": {
                "secret": "password=hunter2",
                "array": ["safe", "/Users/other/.ssh/id_rsa", "token=abc123"]
            }
        }
        clean = self.sanitizer.sanitize_structure(dirty)
        
        self.assertNotIn("devops", clean["user"])
        self.assertNotIn("hunter2", clean["nested"]["secret"])
        self.assertNotIn("other", clean["nested"]["array"][1])
        self.assertNotIn("abc123", clean["nested"]["array"][2])
    
    def test_sanitize_list(self):
        """Verify list sanitization."""
        dirty = [
            "/Users/test/path",
            "safe_string_123",
            "api_key=secretvalue"
        ]
        clean = self.sanitizer.sanitize_structure(dirty)
        
        self.assertNotIn("test", clean[0])
        self.assertEqual(clean[1], "safe_string_123")
        self.assertNotIn("secretvalue", clean[2])
    
    # ---- Edge Cases ----
    
    def test_handles_non_strings_gracefully(self):
        """Verify non-string inputs pass through."""
        self.assertEqual(self.sanitizer.sanitize_string(123), 123)
        self.assertEqual(self.sanitizer.sanitize_string(None), None)
        self.assertEqual(self.sanitizer.sanitize_string(True), True)
    
    def test_empty_string_passthrough(self):
        """Verify empty strings pass through."""
        self.assertEqual(self.sanitizer.sanitize_string(""), "")
    
    def test_pattern_count(self):
        """Verify pattern count matches expected."""
        self.assertGreater(self.sanitizer.get_pattern_count(), 0)
    
    def test_custom_pattern_addition(self):
        """Verify custom patterns can be added."""
        import re
        self.sanitizer.add_pattern(r"CUSTOM_SECRET_\w+", "[CUSTOM_REDACTED]")
        
        input_str = "Found CUSTOM_SECRET_12345 in log"
        result = self.sanitizer.sanitize_string(input_str)
        
        self.assertNotIn("CUSTOM_SECRET_12345", result)
        self.assertIn("[CUSTOM_REDACTED]", result)


if __name__ == "__main__":
    unittest.main()
