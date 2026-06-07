"""
MIF Configuration Module
Contains all schemas, constants, and pattern definitions.
"""

import re

# =====================================================================
# SYSTEM SNAPSHOT JSON SCHEMA DEFINITION (Draft 7 compatible)
# =====================================================================
SYSTEM_SNAPSHOT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "CleanSystemSnapshot",
    "type": "object",
    "properties": {
        "system_metadata": {
            "type": "object",
            "properties": {
                "os_platform": {"type": "string"},
                "kernel_version": {"type": "string"},
                "hostname": {"type": "string"},
                "timestamp": {"type": "string"},
                "collection_duration_ms": {"type": "number"}
            },
            "required": ["os_platform", "kernel_version", "timestamp"]
        },
        "packages": {
            "type": "object",
            "properties": {
                "system_level": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "language_runtimes": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "required": ["system_level", "language_runtimes"]
        }
    },
    "required": ["system_metadata", "packages"]
}

# =====================================================================
# SANITIZATION PATTERNS
# =====================================================================
SENSITIVE_PATTERNS = [
    # Credentials and secrets
    (re.compile(r"(?i)(passwd|password|secret|token|api_key|apikey|auth_token|access_token|private_key)\s*[:=]\s*\S+", re.IGNORECASE), r"\1=[REDACTED_SECRET]"),
    # User home directories - macOS
    (re.compile(r"/Users/[a-zA-Z0-9_\-\.]+"), "/Users/[REDACTED_USER]"),
    # User home directories - Linux
    (re.compile(r"/home/[a-zA-Z0-9_\-\.]+"), "/home/[REDACTED_USER]"),
    # SSH key paths
    (re.compile(r"/\.(ssh|gnupg)/[^\s\"']+"), "/.[REDACTED_KEY_PATH]/[REDACTED]"),
    # IP addresses (IPv4)
    (re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"), "[REDACTED_IP]"),
    # Email addresses
    (re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"), "[REDACTED_EMAIL]"),
    # UUIDs
    (re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b"), "[REDACTED_UUID]"),
    # AWS Keys
    (re.compile(r"(?i)(AKIA[0-9A-Z]{16})"), "[REDACTED_AWS_KEY]"),
    # Generic connection strings with passwords
    (re.compile(r"(?i)(://[^:]+:)[^@]+(@)"), r"\1[REDACTED]\2"),
]

# =====================================================================
# SUPPORTED PLATFORMS
# =====================================================================
SUPPORTED_PLATFORMS = ["linux", "darwin"]

# =====================================================================
# LINUX DISTRO DETECTION MAP
# =====================================================================
DISTRO_PACKAGE_MANAGERS = {
    "debian": ["dpkg-query", "-W", "-f=${Package} ${Version}\n"],
    "ubuntu": ["dpkg-query", "-W", "-f=${Package} ${Version}\n"],
    "linuxmint": ["dpkg-query", "-W", "-f=${Package} ${Version}\n"],
    "fedora": ["rpm", "-qa", "--queryformat", "%{NAME} %{VERSION}\n"],
    "centos": ["rpm", "-qa", "--queryformat", "%{NAME} %{VERSION}\n"],
    "rhel": ["rpm", "-qa", "--queryformat", "%{NAME} %{VERSION}\n"],
    "arch": ["pacman", "-Q"],
    "manjaro": ["pacman", "-Q"],
}
