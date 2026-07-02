#!/usr/bin/env python3
"""
Final Verification Script
Run after all files are created to verify MIF compliance.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_imports():
    """Verify all modules can be imported."""
    print("[VERIFY] Testing imports...")
    try:
        from mif_env_mapper import (
            Orchestrator,
            DiscoveryEngine,
            DataSanitizer,
            SchemaValidator,
            Reporter,
            SYSTEM_SNAPSHOT_SCHEMA
        )
        print("[PASS] All imports successful")
        return True
    except ImportError as e:
        print(f"[FAIL] Import error: {e}")
        return False

def verify_no_external_deps():
    """Verify no external packages are imported."""
    print("[VERIFY] Checking for external dependencies...")
    
    stdlib_modules = {
        'os', 'sys', 're', 'json', 'platform', 'subprocess', 'datetime',
        'typing', 'unittest', 'argparse', 'logging', 'time', 'io',
        'collections', 'pathlib', 'textwrap', 'functools', 'itertools',
        'contextlib', 'tempfile', 'shutil', 'socket', 'struct',
        'hashlib', 'base64', 'urllib', 'http', 'email', 'html',
        'xml', 'csv', 'configparser', 'getopt', 'unittest'
    }
    
    project_files = []
    for root, dirs, files in os.walk('mif_env_mapper'):
        for f in files:
            if f.endswith('.py'):
                project_files.append(os.path.join(root, f))
    
    external_found = []
    for filepath in project_files:
        with open(filepath, 'r') as f:
            content = f.read()
            # Check for import statements, skip comments
            for line in content.split('\n'):
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith('#'):
                    continue
                if line.startswith('import ') or line.startswith('from '):
                    parts = line.split()
                    if len(parts) >= 2:
                        module = parts[1].split('.')[0]
                        # Skip empty module names and local imports
                        if module and module not in stdlib_modules and not module.startswith('mif_'):
                            external_found.append((filepath, module))
    
    if external_found:
        print("[FAIL] External dependencies found:")
        for filepath, module in external_found:
            print(f"  {filepath}: {module}")
        return False
    
    print("[PASS] No external dependencies found")
    return True

def verify_schema_validation():
    """Verify schema validation works correctly."""
    print("[VERIFY] Testing schema validation...")
    from mif_env_mapper import SchemaValidator, SYSTEM_SNAPSHOT_SCHEMA
    
    validator = SchemaValidator()
    
    # Valid data should pass
    valid_data = {
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
    
    if not validator.validate(valid_data, SYSTEM_SNAPSHOT_SCHEMA):
        print("[FAIL] Valid data rejected")
        return False
    
    # Invalid data should fail
    invalid_data = {"wrong": "structure"}
    if validator.validate(invalid_data, SYSTEM_SNAPSHOT_SCHEMA):
        print("[FAIL] Invalid data accepted")
        return False
    
    print("[PASS] Schema validation working correctly")
    return True

def verify_sanitization():
    """Verify PII sanitization works."""
    print("[VERIFY] Testing PII sanitization...")
    from mif_env_mapper import DataSanitizer
    
    sanitizer = DataSanitizer()
    
    test_cases = [
        ("/Users/johndoe/path", "johndoe"),
        ("/home/janedoe/file", "janedoe"),
        ("password=secret123", "secret123"),
        ("auth_token=abc123", "abc123"),
        ("192.168.1.1", "[REDACTED_IP]"),
    ]
    
    for input_str, should_not_contain in test_cases:
        result = sanitizer.sanitize_string(input_str)
        if should_not_contain in result:
            print(f"[FAIL] PII leak: '{should_not_contain}' found in '{result}'")
            return False
    
    print("[PASS] PII sanitization working correctly")
    return True

def verify_subprocess_safety():
    """Verify no shell=True in subprocess calls."""
    print("[VERIFY] Checking subprocess safety...")
    
    for root, dirs, files in os.walk('mif_env_mapper'):
        for f in files:
            if f.endswith('.py'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r') as file:
                    content = file.read()
                    # Check for shell=True in actual code, not comments/docstrings
                    for line in content.split('\n'):
                        line = line.strip()
                        # Skip comments and docstrings
                        if not line or line.startswith('#') or line.startswith('"""') or line.startswith("'''"):
                            continue
                        # Only check lines that look like subprocess calls
                        if 'subprocess.run' in line or 'subprocess.call' in line or 'subprocess.Popen' in line:
                            if 'shell=True' in line:
                                print(f"[FAIL] shell=True found in subprocess call in {filepath}")
                                return False
    
    print("[PASS] No shell=True found in any subprocess calls")
    return True

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("MIF ENVIRONMENT MAPPER - FINAL VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Imports", verify_imports),
        ("External Dependencies", verify_no_external_deps),
        ("Schema Validation", verify_schema_validation),
        ("PII Sanitization", verify_sanitization),
        ("Subprocess Safety", verify_subprocess_safety),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            results.append((name, False))
        print()
    
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    if all_passed:
        print("ALL CHECKS PASSED - MIF COMPLIANCE VERIFIED")
        return 0
    else:
        print("SOME CHECKS FAILED - REVIEW REQUIRED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
