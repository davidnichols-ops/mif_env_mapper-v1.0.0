"""
Report Generation Module
Handles output formatting and serialization.
"""

import json
import sys
from datetime import datetime
from typing import Any, Dict, Optional, TextIO


class Reporter:
    """
    Formats and outputs environment snapshot data.
    
    Methods:
        format_json(data): Returns formatted JSON string
        format_summary(data): Returns human-readable summary
        write_json(data, output): Writes JSON to file or stdout
        write_summary(data, output): Writes summary to file or stdout
    """
    
    def __init__(self, pretty: bool = True):
        """
        Initialize reporter.
        
        Args:
            pretty: If True, use indented JSON output
        """
        self.pretty = pretty
    
    def format_json(self, data: Dict[str, Any]) -> str:
        """
        Converts data to formatted JSON string.
        
        Args:
            data: Dictionary to serialize
            
        Returns:
            JSON string
        """
        indent = 2 if self.pretty else None
        return json.dumps(data, indent=indent, ensure_ascii=False, default=str)
    
    def format_summary(self, data: Dict[str, Any]) -> str:
        """
        Creates a human-readable summary of the environment snapshot.
        
        Args:
            data: System snapshot dictionary
            
        Returns:
            Formatted summary string
        """
        lines = []
        lines.append("=" * 60)
        lines.append("SYSTEM ENVIRONMENT SNAPSHOT SUMMARY")
        lines.append("=" * 60)
        
        # Metadata
        metadata = data.get("system_metadata", {})
        lines.append(f"\nOperating System: {metadata.get('os_platform', 'Unknown')}")
        lines.append(f"Kernel Version:   {metadata.get('kernel_version', 'Unknown')}")
        lines.append(f"Timestamp:        {metadata.get('timestamp', 'Unknown')}")
        
        if "collection_duration_ms" in metadata:
            lines.append(f"Collection Time:  {metadata['collection_duration_ms']}ms")
        
        # Package counts
        packages = data.get("packages", {})
        sys_count = len(packages.get("system_level", []))
        runtime_count = len(packages.get("language_runtimes", []))
        
        lines.append(f"\nSystem Packages:       {sys_count}")
        lines.append(f"Language Runtime Pkgs: {runtime_count}")
        lines.append(f"Total Packages:        {sys_count + runtime_count}")
        
        # Show first few packages as sample
        sys_pkgs = packages.get("system_level", [])
        if sys_pkgs:
            lines.append(f"\nSample System Packages (first 5):")
            for pkg in sys_pkgs[:5]:
                lines.append(f"  - {pkg}")
        
        rt_pkgs = packages.get("language_runtimes", [])
        if rt_pkgs:
            lines.append(f"\nSample Runtime Packages (first 5):")
            for pkg in rt_pkgs[:5]:
                lines.append(f"  - {pkg}")
        
        lines.append("\n" + "=" * 60)
        
        return "\n".join(lines)
    
    def write_json(self, data: Dict[str, Any], output: Optional[TextIO] = None) -> None:
        """
        Writes JSON output to file or stdout.
        
        Args:
            data: Dictionary to output
            output: File-like object, or None for stdout
        """
        json_str = self.format_json(data)
        if output is None:
            print(json_str)
        else:
            output.write(json_str)
            output.write("\n")
    
    def write_summary(self, data: Dict[str, Any], output: Optional[TextIO] = None) -> None:
        """
        Writes summary output to file or stdout.
        
        Args:
            data: Dictionary to summarize
            output: File-like object, or None for stdout
        """
        summary = self.format_summary(data)
        if output is None:
            print(summary)
        else:
            output.write(summary)
            output.write("\n")
