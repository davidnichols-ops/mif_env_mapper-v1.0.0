"""
Tests for DiscoveryEngine module.
"""

import unittest
import sys
import os
import platform
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mif_env_mapper.engine import DiscoveryEngine


class TestDiscoveryEngine(unittest.TestCase):
    """Test cases for DiscoveryEngine class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.engine = DiscoveryEngine(timeout=5)
    
    # ---- Command Execution Tests ----
    
    def test_execute_command_success(self):
        """Verify successful command execution returns output."""
        result = self.engine.execute_command(["echo", "hello world"])
        self.assertIn("hello world", result)
    
    def test_execute_command_not_found(self):
        """Verify missing command returns empty list."""
        result = self.engine.execute_command(["nonexistent_command_xyz_123"])
        self.assertEqual(result, [])
        self.assertGreater(len(self.engine.errors), 0)
    
    def test_execute_command_error(self):
        """Verify failing command returns empty list."""
        result = self.engine.execute_command(["false"])
        self.assertEqual(result, [])
    
    # ---- Error Management Tests ----
    
    def test_errors_property_returns_copy(self):
        """Verify errors property returns a copy."""
        self.engine.execute_command(["nonexistent_cmd_xyz"])
        errors = self.engine.errors
        errors.clear()  # Should not affect internal state
        self.assertGreater(len(self.engine.errors), 0)
    
    def test_clear_errors(self):
        """Verify error clearing works."""
        self.engine.execute_command(["nonexistent_cmd_xyz"])
        self.assertGreater(len(self.engine.errors), 0)
        self.engine.clear_errors()
        self.assertEqual(len(self.engine.errors), 0)
    
    # ---- System Info Tests ----
    
    def test_get_system_info_returns_required_fields(self):
        """Verify system info contains required fields."""
        info = self.engine.get_system_info()
        
        self.assertIn("os_platform", info)
        self.assertIn("kernel_version", info)
        self.assertIn("hostname", info)
        self.assertIn("architecture", info)
    
    def test_platform_is_normalized(self):
        """Verify platform is normalized to linux/darwin/unknown."""
        info = self.engine.get_system_info()
        self.assertIn(info["os_platform"], ["linux", "darwin", "unknown"])
    
    # ---- Package Collection Tests (Mocked) ----
    
    @patch.object(DiscoveryEngine, 'execute_command')
    def test_gather_packages_darwin(self, mock_cmd):
        """Verify Darwin package collection calls brew commands."""
        mock_cmd.return_value = ["package1 1.0", "package2 2.0"]
        
        result = self.engine.gather_packages("darwin")
        
        self.assertIn("system_level", result)
        self.assertIn("language_runtimes", result)
        # Verify brew commands were called
        self.assertTrue(mock_cmd.called)
    
    @patch.object(DiscoveryEngine, 'execute_command')
    @patch.object(DiscoveryEngine, '_get_linux_distro')
    def test_gather_packages_linux(self, mock_distro, mock_cmd):
        """Verify Linux package collection uses detected distro."""
        mock_distro.return_value = "ubuntu"
        mock_cmd.return_value = ["package1 1.0-1", "package2 2.0-1"]
        
        result = self.engine.gather_packages("linux")
        
        self.assertIn("system_level", result)
        self.assertIn("language_runtimes", result)


if __name__ == "__main__":
    unittest.main()
