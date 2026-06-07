"""
🧪 Tests for Easy Tools - Simple tests for simple functions!
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from easy_tools import (
    hide_secrets_in_string,
    hide_secrets_in_list,
    hide_secrets_in_dict,
    make_computer_info,
    make_report,
    check_report_is_good
)


class TestSecretHiding(unittest.TestCase):
    """Test that we hide secrets properly."""
    
    def test_hides_mac_user_paths(self):
        """Hide /Users/ paths."""
        result = hide_secrets_in_string("/Users/john/myfile")
        self.assertIn("[HIDDEN]", result)
        self.assertNotIn("john", result)
    
    def test_hides_linux_home_paths(self):
        """Hide /home/ paths."""
        result = hide_secrets_in_string("/home/jane/myfile")
        self.assertIn("[HIDDEN]", result)
        self.assertNotIn("jane", result)
    
    def test_hides_passwords(self):
        """Hide passwords."""
        result = hide_secrets_in_string("password=secret123")
        self.assertIn("[HIDDEN]", result)
        self.assertNotIn("secret123", result)
    
    def test_hides_tokens(self):
        """Hide tokens."""
        result = hide_secrets_in_string("token=abc123")
        self.assertIn("[HIDDEN]", result)
        self.assertNotIn("abc123", result)
    
    def test_hides_api_keys(self):
        """Hide API keys."""
        result = hide_secrets_in_string("api_key=xyz789")
        self.assertIn("[HIDDEN]", result)
        self.assertNotIn("xyz789", result)
    
    def test_hides_secrets_in_list(self):
        """Hide secrets in a list."""
        dirty = ["/Users/john/file", "password=secret", "safe text"]
        clean = hide_secrets_in_list(dirty)
        
        self.assertNotIn("john", clean[0])
        self.assertNotIn("secret", clean[1])
        self.assertEqual(clean[2], "safe text")
    
    def test_hides_secrets_in_dict(self):
        """Hide secrets in a dictionary."""
        dirty = {
            "path": "/Users/john/config",
            "secret": "password=secret123",
            "safe": "hello"
        }
        clean = hide_secrets_in_dict(dirty)
        
        self.assertNotIn("john", clean["path"])
        self.assertNotIn("secret123", clean["secret"])
        self.assertEqual(clean["safe"], "hello")


class TestReportMaking(unittest.TestCase):
    """Test report making functions."""
    
    def test_computer_info_has_required_fields(self):
        """Computer info should have all required fields."""
        info = make_computer_info()
        
        self.assertIn("type", info)
        self.assertIn("name", info)
        self.assertIn("kernel", info)
        self.assertIn("machine", info)
        self.assertIn("time", info)
    
    def test_make_report_structure(self):
        """Report should have correct structure."""
        packages = {
            "system": ["pkg1 1.0", "pkg2 2.0"],
            "apps": ["app1==1.0", "app2==2.0"]
        }
        report = make_report(packages)
        
        self.assertIn("computer", report)
        self.assertIn("packages", report)
        self.assertIn("system", report["packages"])
        self.assertIn("apps", report["packages"])
    
    def test_report_hides_secrets(self):
        """Report should hide secrets."""
        packages = {
            "system": ["/Users/john/pkg"],
            "apps": ["password=secret"]
        }
        report = make_report(packages)
        
        pkg_str = str(report["packages"]["system"])
        self.assertNotIn("john", pkg_str)
        
        app_str = str(report["packages"]["apps"])
        self.assertNotIn("secret", app_str)


class TestReportChecking(unittest.TestCase):
    """Test report checking functions."""
    
    def test_good_report_passes(self):
        """A good report should pass the check."""
        report = {
            "computer": {"type": "darwin"},
            "packages": {
                "system": [],
                "apps": []
            }
        }
        is_good, message = check_report_is_good(report)
        self.assertTrue(is_good)
    
    def test_missing_computer_fails(self):
        """Report without computer info should fail."""
        report = {
            "packages": {
                "system": [],
                "apps": []
            }
        }
        is_good, message = check_report_is_good(report)
        self.assertFalse(is_good)
    
    def test_missing_packages_fails(self):
        """Report without packages should fail."""
        report = {
            "computer": {"type": "darwin"}
        }
        is_good, message = check_report_is_good(report)
        self.assertFalse(is_good)
    
    def test_missing_system_packages_fails(self):
        """Report without system packages should fail."""
        report = {
            "computer": {"type": "darwin"},
            "packages": {
                "apps": []
            }
        }
        is_good, message = check_report_is_good(report)
        self.assertFalse(is_good)
    
    def test_not_a_dict_fails(self):
        """Something that's not a dict should fail."""
        is_good, message = check_report_is_good("not a dict")
        self.assertFalse(is_good)


if __name__ == "__main__":
    unittest.main()
