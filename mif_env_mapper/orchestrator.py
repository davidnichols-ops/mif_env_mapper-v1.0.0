"""
Orchestration Pipeline Module
Coordinates the full environment mapping workflow.
"""

import logging
import platform
import sys
from datetime import datetime
from typing import Any, Dict, Optional

from .config import SYSTEM_SNAPSHOT_SCHEMA, SUPPORTED_PLATFORMS
from .engine import DiscoveryEngine
from .sanitizer import DataSanitizer
from .validator import SchemaValidator
from .reporter import Reporter

logger = logging.getLogger(__name__)


class OrchestrationError(Exception):
    """Raised when the pipeline encounters a fatal error."""
    pass


class Orchestrator:
    """
    Coordinates the full MIF environment mapping pipeline.
    
    Pipeline Steps:
        1. Detect OS platform
        2. Gather package data
        3. Collect system metadata
        4. Sanitize all data
        5. Validate against schema
        6. Output formatted result
    
    Methods:
        run(): Execute full pipeline, returns JSON string
        run_silent(): Execute pipeline, returns dict (no output)
    """
    
    def __init__(self, timeout: int = 30, pretty_output: bool = True):
        """
        Initialize the orchestrator with all pipeline components.
        
        Args:
            timeout: Subprocess timeout in seconds
            pretty_output: Whether to format JSON output with indentation
        """
        self.sanitizer = DataSanitizer()
        self.discovery = DiscoveryEngine(timeout=timeout)
        self.validator = SchemaValidator()
        self.reporter = Reporter(pretty=pretty_output)
        self._duration_ms: float = 0.0
    
    @property
    def duration_ms(self) -> float:
        """Duration of last pipeline run in milliseconds."""
        return self._duration_ms
    
    def _detect_platform(self) -> str:
        """
        Detect and normalize the current OS platform.
        
        Returns:
            'linux' or 'darwin'
            
        Raises:
            OrchestrationError: If platform is not supported
        """
        raw_os = platform.system().lower()
        normalized_os = "linux" if raw_os == "linux" else ("darwin" if raw_os == "darwin" else "unknown")
        
        if normalized_os == "unknown" or normalized_os not in SUPPORTED_PLATFORMS:
            raise OrchestrationError(
                f"Operating system platform '{raw_os}' is not supported. "
                f"Supported platforms: {', '.join(SUPPORTED_PLATFORMS)}"
            )
        
        return normalized_os
    
    def _build_snapshot(self, os_type: str) -> Dict[str, Any]:
        """
        Build the complete system snapshot dictionary.
        
        Args:
            os_type: 'linux' or 'darwin'
            
        Returns:
            Complete snapshot dictionary
        """
        import time
        start_time = time.time()
        
        # Gather package data
        logger.info("Starting package discovery...")
        raw_packages = self.discovery.gather_packages(os_type)
        
        # Collect system metadata
        logger.info("Collecting system metadata...")
        sys_info = self.discovery.get_system_info()
        
        # Calculate duration
        end_time = time.time()
        self._duration_ms = round((end_time - start_time) * 1000, 2)
        
        raw_payload = {
            "system_metadata": {
                "os_platform": sys_info["os_platform"],
                "kernel_version": sys_info["kernel_version"],
                "hostname": sys_info.get("hostname", ""),
                "architecture": sys_info.get("architecture", ""),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "collection_duration_ms": self._duration_ms
            },
            "packages": raw_packages
        }
        
        return raw_payload
    
    def _sanitize_snapshot(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply data sanitization to the snapshot.
        
        Args:
            data: Raw snapshot data
            
        Returns:
            Sanitized snapshot data
        """
        logger.info("Applying data sanitization...")
        return self.sanitizer.sanitize_structure(data)
    
    def _validate_snapshot(self, data: Dict[str, Any]) -> None:
        """
        Validate snapshot against schema.
        
        Args:
            data: Snapshot to validate
            
        Raises:
            OrchestrationError: If validation fails
        """
        logger.info("Validating against schema...")
        errors = self.validator.validate_with_errors(data, SYSTEM_SNAPSHOT_SCHEMA)
        
        if errors:
            error_msg = "MIF Pipeline Failure: Generated snapshot failed structural validation:\n"
            for err in errors:
                error_msg += f"  - {err}\n"
            raise OrchestrationError(error_msg)
    
    def run(self) -> str:
        """
        Execute the full pipeline and return JSON string.
        
        Returns:
            Complete sanitized, validated JSON snapshot
            
        Raises:
            OrchestrationError: On pipeline failures
        """
        try:
            # Step 1: Platform detection
            os_type = self._detect_platform()
            
            # Step 2-3: Build snapshot
            raw_payload = self._build_snapshot(os_type)
            
            # Step 4: Sanitize
            clean_payload = self._sanitize_snapshot(raw_payload)
            
            # Step 5: Validate
            self._validate_snapshot(clean_payload)
            
            # Step 6: Format output
            return self.reporter.format_json(clean_payload)
            
        except OrchestrationError:
            raise
        except Exception as e:
            raise OrchestrationError(f"Unexpected pipeline error: {str(e)}") from e
    
    def run_silent(self) -> Dict[str, Any]:
        """
        Execute the full pipeline and return dictionary.
        
        Returns:
            Complete sanitized, validated snapshot dictionary
        """
        os_type = self._detect_platform()
        raw_payload = self._build_snapshot(os_type)
        clean_payload = self._sanitize_snapshot(raw_payload)
        self._validate_snapshot(clean_payload)
        return clean_payload
