#!/usr/bin/env python3
"""
Verification for Easy Mode
Check that the simplified version still meets safety requirements.
"""

import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def verify_imports():
    """Verify easy modules can be imported."""
    print("[VERIFY] Testing easy mode imports...")
    try:
        import easy_tools
        print("[PASS] easy_tools imported successfully")
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
    
    project_files = ['easy_main.py', 'easy_tools.py']
    external_found = []
    
    for filepath in project_files:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r') as f:
            content = f.read()
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if line.startswith('import ') or line.startswith('from '):
                    parts = line.split()
                    if len(parts) >= 2:
                        module = parts[1].split('.')[0]
                        if module and module not in stdlib_modules and not module.startswith('easy_'):
                            external_found.append((filepath, module))
    
    if external_found:
        print("[FAIL] External dependencies found:")
        for filepath, module in external_found:
            print(f"  {filepath}: {module}")
        return False
    
    print("[PASS] No external dependencies found")
    return True

def verify_subprocess_safety():
    """Verify no shell=True in subprocess calls."""
    print("[VERIFY] Checking subprocess safety...")
    
    project_files = ['easy_main.py', 'easy_tools.py']
    
    for filepath in project_files:
        if not os.path.exists(filepath):
            continue
        with open(filepath, 'r') as file:
            content = file.read()
            for line in content.split('\n'):
                line = line.strip()
                if not line or line.startswith('#') or line.startswith('"""') or line.startswith("'''"):
                    continue
                if 'subprocess.run' in line or 'subprocess.call' in line or 'subprocess.Popen' in line:
                    if 'shell=True' in line:
                        print(f"[FAIL] shell=True found in subprocess call in {filepath}")
                        return False
    
    print("[PASS] No shell=True found in any subprocess calls")
    return True

def verify_secret_hiding():
    """Verify secret hiding works."""
    print("[VERIFY] Testing secret hiding...")
    from easy_tools import hide_secrets_in_string
    
    test_cases = [
        ("/Users/john/path", "john"),
        ("/home/jane/file", "jane"),
        ("password=secret123", "secret123"),
        ("token=abc123", "abc123"),
    ]
    
    for input_str, should_not_contain in test_cases:
        result = hide_secrets_in_string(input_str)
        if should_not_contain in result:
            print(f"[FAIL] Secret leak: '{should_not_contain}' found in '{result}'")
            return False
    
    print("[PASS] Secret hiding working correctly")
    return True

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("EASY MODE VERIFICATION")
    print("=" * 60)
    
    checks = [
        ("Imports", verify_imports),
        ("External Dependencies", verify_no_external_deps),
        ("Subprocess Safety", verify_subprocess_safety),
        ("Secret Hiding", verify_secret_hiding),
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
        print("ALL CHECKS PASSED - EASY MODE IS SAFE")
        return 0
    else:
        print("SOME CHECKS FAILED - REVIEW REQUIRED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
