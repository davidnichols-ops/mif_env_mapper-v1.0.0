"""
Tests for Orchestrator module.
"""

import unittest
import sys
import os
import json
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mif_env_mapper.orchestrator import Orchestrator, OrchestrationError


class TestOrchestrator(unittest.TestCase):
    """Test cases for Orchestrator class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.orchestrator = Orchestrator(timeout=5, pretty_output=False)
    
    # ---- Platform Detection Tests ----
    
    @patch('mif_env_mapper.orchestrator.platform')
    def test_detect_platform_linux(self, mock_platform):
        """Verify Linux platform detection."""
        mock_platform.system.return_value = "Linux"
        result = self.orchestrator._detect_platform()
        self.assertEqual(result, "linux")
    
    @patch('mif_env_mapper.orchestrator.platform')
    def test_detect_platform_darwin(self, mock_platform):
        """Verify Darwin platform detection."""
        mock_platform.system.return_value = "Darwin"
        result = self.orchestrator._detect_platform()
        self.assertEqual(result, "darwin")
    
    @patch('mif_env_mapper.orchestrator.platform')
    def test_detect_platform_unknown_raises(self, mock_platform):
        """Verify unknown platform raises error."""
        mock_platform.system.return_value = "Windows"
        with self.assertRaises(OrchestrationError):
            self.orchestrator._detect_platform()
    
    # ---- Snapshot Building Tests ----
    
    @patch('mif_env_mapper.orchestrator.DiscoveryEngine')
    def test_build_snapshot_structure(self, mock_engine_cls):
        """Verify snapshot has correct structure."""
        mock_engine = MagicMock()
        mock_engine.gather_packages.return_value = {
            "system_level": ["pkg1 1.0"],
            "language_runtimes": []
        }
        mock_engine.get_system_info.return_value = {
            "os_platform": "linux",
            "kernel_version": "5.15.0",
            "hostname": "testhost",
            "architecture": "x86_64"
        }
        mock_engine.errors = []
        
        self.orchestrator.discovery = mock_engine
        
        snapshot = self.orchestrator._build_snapshot("linux")
        
        # Verify structure
        self.assertIn("system_metadata", snapshot)
        self.assertIn("packages", snapshot)
        self.assertIn("os_platform", snapshot["system_metadata"])
        self.assertIn("kernel_version", snapshot["system_metadata"])
        self.assertIn("timestamp", snapshot["system_metadata"])
        self.assertIn("collection_duration_ms", snapshot["system_metadata"])
        self.assertIn("system_level", snapshot["packages"])
        self.assertIn("language_runtimes", snapshot["packages"])
    
    # ---- Sanitization Tests ----
    
    def test_sanitize_snapshot_removes_pii(self):
        """Verify sanitization removes PII from snapshot."""
        dirty_snapshot = {
            "system_metadata": {
                "os_platform": "linux",
                "kernel_version": "5.15.0",
                "timestamp": "2026-06-07T16:20:00Z",
                "hostname": "testhost"
            },
            "packages": {
                "system_level": ["/Users/johndoe/app 1.0"],
                "language_runtimes": ["pip 22.0"]
            }
        }
        
        clean = self.orchestrator._sanitize_snapshot(dirty_snapshot)
        
        # Verify PII is removed
        pkg_str = str(clean["packages"]["system_level"])
        self.assertNotIn("johndoe", pkg_str)
    
    # ---- Validation Tests ----
    
    def test_validate_snapshot_rejects_invalid(self):
        """Verify validation rejects invalid snapshot."""
        invalid_snapshot = {
            "system_metadata": "should_be_object",
            "packages": {}
        }
        
        with self.assertRaises(OrchestrationError):
            self.orchestrator._validate_snapshot(invalid_snapshot)
    
    def test_validate_snapshot_accepts_valid(self):
        """Verify validation accepts valid snapshot."""
        valid_snapshot = {
            "system_metadata": {
                "os_platform": "linux",
                "kernel_version": "5.15.0",
                "timestamp": "2026-06-07T16:20:00Z"
            },
            "packages": {
                "system_level": ["bash 5.1"],
                "language_runtimes": ["pip 22.0"]
            }
        }
        
        # Should not raise
        self.orchestrator._validate_snapshot(valid_snapshot)
    
    # ---- Full Pipeline Tests (Mocked) ----
    
    @patch.object(Orchestrator, '_detect_platform')
    @patch.object(Orchestrator, '_build_snapshot')
    @patch.object(Orchestrator, '_sanitize_snapshot')
    @patch.object(Orchestrator, '_validate_snapshot')
    def test_run_returns_json_string(self, mock_validate, mock_sanitize, mock_build, mock_detect):
        """Verify run() returns valid JSON string."""
        mock_detect.return_value = "linux"
        mock_build.return_value = {
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
        mock_sanitize.return_value = mock_build.return_value
        
        result = self.orchestrator.run()
        
        # Verify it's valid JSON
        parsed = json.loads(result)
        self.assertIn("system_metadata", parsed)
        self.assertIn("packages", parsed)
    
    @patch.object(Orchestrator, '_detect_platform')
    @patch.object(Orchestrator, '_build_snapshot')
    @patch.object(Orchestrator, '_sanitize_snapshot')
    @patch.object(Orchestrator, '_validate_snapshot')
    def test_run_silent_returns_dict(self, mock_validate, mock_sanitize, mock_build, mock_detect):
        """Verify run_silent() returns dictionary."""
        mock_detect.return_value = "linux"
        mock_build.return_value = {
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
        mock_sanitize.return_value = mock_build.return_value
        
        result = self.orchestrator.run_silent()
        
        self.assertIsInstance(result, dict)
        self.assertIn("system_metadata", result)
    
    # ---- Duration Tracking Tests ----
    
    def test_duration_initialized_to_zero(self):
        """Verify duration starts at zero."""
        self.assertEqual(self.orchestrator.duration_ms, 0.0)
    
    @patch('mif_env_mapper.orchestrator.DiscoveryEngine')
    def test_duration_set_after_build(self, mock_engine_cls):
        """Verify duration is set after building snapshot."""
        mock_engine = MagicMock()
        mock_engine.gather_packages.return_value = {"system_level": [], "language_runtimes": []}
        mock_engine.get_system_info.return_value = {
            "os_platform": "linux",
            "kernel_version": "5.15.0",
            "hostname": "",
            "architecture": ""
        }
        mock_engine.errors = []
        
        self.orchestrator.discovery = mock_engine
        self.orchestrator._build_snapshot("linux")
        
        self.assertGreater(self.orchestrator.duration_ms, 0)


if __name__ == "__main__":
    unittest.main()
