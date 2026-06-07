"""
Tests for SchemaValidator module.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mif_env_mapper.validator import SchemaValidator
from mif_env_mapper.config import SYSTEM_SNAPSHOT_SCHEMA


class TestSchemaValidator(unittest.TestCase):
    """Test cases for SchemaValidator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.validator = SchemaValidator()
    
    # ---- Type Check Tests ----
    
    def test_string_type_check(self):
        """Verify string type validation."""
        self.assertTrue(self.validator.check_type("hello", "string"))
        self.assertFalse(self.validator.check_type(123, "string"))
    
    def test_integer_type_check(self):
        """Verify integer type validation."""
        self.assertTrue(self.validator.check_type(42, "integer"))
        self.assertFalse(self.validator.check_type("42", "integer"))
        self.assertFalse(self.validator.check_type(3.14, "integer"))
    
    def test_boolean_not_integer(self):
        """Verify bool is not accepted as integer."""
        self.assertFalse(self.validator.check_type(True, "integer"))
        self.assertFalse(self.validator.check_type(False, "integer"))
    
    def test_array_type_check(self):
        """Verify array type validation."""
        self.assertTrue(self.validator.check_type([], "array"))
        self.assertTrue(self.validator.check_type([1, 2, 3], "array"))
        self.assertFalse(self.validator.check_type({}, "array"))
    
    def test_object_type_check(self):
        """Verify object type validation."""
        self.assertTrue(self.validator.check_type({}, "object"))
        self.assertTrue(self.validator.check_type({"key": "val"}, "object"))
        self.assertFalse(self.validator.check_type([], "object"))
    
    # ---- Schema Validation Tests ----
    
    def test_valid_snapshot_passes(self):
        """Verify valid snapshot data passes validation."""
        valid_snapshot = {
            "system_metadata": {
                "os_platform": "linux",
                "kernel_version": "5.15.0",
                "timestamp": "2026-06-07T16:20:00Z"
            },
            "packages": {
                "system_level": ["bash 5.1", "python3 3.10"],
                "language_runtimes": ["pip 22.0", "numpy 1.24"]
            }
        }
        self.assertTrue(self.validator.validate(valid_snapshot, SYSTEM_SNAPSHOT_SCHEMA))
    
    def test_missing_required_key_fails(self):
        """Verify missing required key fails validation."""
        invalid_snapshot = {
            "system_metadata": {
                "os_platform": "linux",
                "kernel_version": "5.15.0"
            }
            # Missing "packages"
        }
        self.assertFalse(self.validator.validate(invalid_snapshot, SYSTEM_SNAPSHOT_SCHEMA))
    
    def test_missing_timestamp_fails(self):
        """Verify missing required timestamp fails."""
        invalid_snapshot = {
            "system_metadata": {
                "os_platform": "linux",
                "kernel_version": "5.15.0"
                # Missing "timestamp"
            },
            "packages": {
                "system_level": [],
                "language_runtimes": []
            }
        }
        self.assertFalse(self.validator.validate(invalid_snapshot, SYSTEM_SNAPSHOT_SCHEMA))
    
    def test_wrong_type_fails(self):
        """Verify wrong field type fails validation."""
        invalid_snapshot = {
            "system_metadata": {
                "os_platform": "linux",
                "kernel_version": "5.15.0",
                "timestamp": "2026-06-07T16:20:00Z"
            },
            "packages": "not_an_object_fails"
        }
        self.assertFalse(self.validator.validate(invalid_snapshot, SYSTEM_SNAPSHOT_SCHEMA))
    
    # ---- Error Message Tests ----
    
    def test_validation_errors_list(self):
        """Verify error messages are descriptive."""
        invalid_snapshot = {
            "system_metadata": "should_be_object",
            "packages": {}
        }
        errors = self.validator.validate_with_errors(invalid_snapshot, SYSTEM_SNAPSHOT_SCHEMA)
        
        self.assertGreater(len(errors), 0)
        # Check that errors mention path
        self.assertIn("$", errors[0])
    
    def test_valid_returns_empty_errors(self):
        """Verify valid data returns no errors."""
        valid_snapshot = {
            "system_metadata": {
                "os_platform": "linux",
                "kernel_version": "5.15.0",
                "timestamp": "2026-06-07T16:20:00Z"
            },
            "packages": {
                "system_level": [],
                "language_runtimes": []
            }
        }
        errors = self.validator.validate_with_errors(valid_snapshot, SYSTEM_SNAPSHOT_SCHEMA)
        self.assertEqual(len(errors), 0)


if __name__ == "__main__":
    unittest.main()
