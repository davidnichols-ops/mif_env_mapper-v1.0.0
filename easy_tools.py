"""
🛠️ Easy Tools - Simple functions for the MIF Environment Mapper
No classes, just simple functions that are easy to understand!
"""

import os
import sys
import platform
import subprocess
import json
from datetime import datetime

# 🔍 Package Finding Functions

def what_computer():
    """Find out what kind of computer this is."""
    return platform.system().lower()

def run_command(cmd):
    """Run a command and get the output. Returns a list of lines."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        lines = result.stdout.strip().split('\n') if result.stdout else []
        # Remove empty lines
        return [line for line in lines if line]
    except subprocess.TimeoutExpired:
        print("⏰ Command took too long!")
        return []
    except FileNotFoundError:
        print(f"❓ Command not found: {cmd[0]}")
        return []
    except Exception as e:
        print(f"😢 Error running command: {e}")
        return []

def find_mac_packages():
    """Find packages on a Mac using Homebrew."""
    packages = []
    
    # Homebrew formulae
    brew_list = run_command(["brew", "list", "--versions"])
    packages.extend(brew_list)
    
    # Homebrew casks
    brew_casks = run_command(["brew", "list", "--casks", "--versions"])
    packages.extend(brew_casks)
    
    return packages

def find_linux_packages():
    """Find packages on Linux."""
    packages = []
    
    # Try different package managers
    package_managers = [
        ["dpkg-query", "-W", "-f=${Package} ${Version}\n"],  # Debian/Ubuntu
        ["rpm", "-qa", "--queryformat", "%{NAME} %{VERSION}\n"],  # Fedora/RHEL
        ["pacman", "-Q"],  # Arch
    ]
    
    for cmd in package_managers:
        result = run_command(cmd)
        if result:
            packages.extend(result)
            break  # Stop if one works
    
    return packages

def find_python_packages():
    """Find Python packages using pip."""
    return run_command([sys.executable, "-m", "pip", "freeze"])

def find_node_packages():
    """Find Node.js packages using npm."""
    npm_list = run_command(["npm", "list", "-g", "--depth=0", "--parseable"])
    # Just get the package names
    return [os.path.basename(p) for p in npm_list if p]

def find_all_packages():
    """Find ALL packages on the computer."""
    computer_type = what_computer()
    
    system_pkgs = []
    app_pkgs = []
    
    # System packages
    if computer_type == "darwin":
        print("🍎 Looking for Mac packages...")
        system_pkgs = find_mac_packages()
    elif computer_type == "linux":
        print("🐧 Looking for Linux packages...")
        system_pkgs = find_linux_packages()
    else:
        print(f"🤔 Unknown computer type: {computer_type}")
    
    # App packages (programming languages)
    print("📦 Looking for app packages...")
    app_pkgs.extend(find_python_packages())
    app_pkgs.extend(find_node_packages())
    
    return {"system": system_pkgs, "apps": app_pkgs}

# 🎨 Secret Hiding Functions

def hide_secrets_in_string(text):
    """Hide secret information like passwords and user names."""
    if not isinstance(text, str):
        return text
    
    # Hide user paths - use regex to match the username too
    import re
    text = re.sub(r'/Users/[a-zA-Z0-9_\-\.]+', '/Users/[HIDDEN]', text)
    text = re.sub(r'/home/[a-zA-Z0-9_\-\.]+', '/home/[HIDDEN]', text)
    
    # Hide passwords
    if "password=" in text.lower():
        parts = text.split("password=", 1)
        if len(parts) > 1:
            # Get the password value (everything until next space or end)
            password_part = parts[1].split()[0] if parts[1].split() else parts[1]
            text = text.replace("password=" + password_part, "password=[HIDDEN]", 1)
    
    # Hide tokens
    if "token=" in text.lower():
        parts = text.split("token=", 1)
        if len(parts) > 1:
            token_part = parts[1].split()[0] if parts[1].split() else parts[1]
            text = text.replace("token=" + token_part, "token=[HIDDEN]", 1)
    
    # Hide API keys
    if "api_key=" in text.lower():
        parts = text.split("api_key=", 1)
        if len(parts) > 1:
            key_part = parts[1].split()[0] if parts[1].split() else parts[1]
            text = text.replace("api_key=" + key_part, "api_key=[HIDDEN]", 1)
    
    return text

def hide_secrets_in_list(items):
    """Hide secrets in a list of strings."""
    return [hide_secrets_in_string(item) for item in items]

def hide_secrets_in_dict(data):
    """Hide secrets in a dictionary (goes through all values)."""
    clean_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            clean_data[key] = hide_secrets_in_string(value)
        elif isinstance(value, list):
            clean_data[key] = hide_secrets_in_list(value)
        elif isinstance(value, dict):
            clean_data[key] = hide_secrets_in_dict(value)
        else:
            clean_data[key] = value
    return clean_data

# 📊 Report Making Functions

def make_computer_info():
    """Get information about the computer."""
    return {
        "type": what_computer(),
        "name": platform.node(),
        "kernel": platform.release(),
        "machine": platform.machine(),
        "time": datetime.now().isoformat()
    }

def make_report(packages):
    """Make a nice report of all the packages."""
    return {
        "computer": make_computer_info(),
        "packages": {
            "system": hide_secrets_in_list(packages["system"]),
            "apps": hide_secrets_in_list(packages["apps"])
        }
    }

def save_report_to_file(report, filename):
    """Save the report to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    return True

def load_report_from_file(filename):
    """Load a report from a JSON file."""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❓ File not found: {filename}")
        return None
    except json.JSONDecodeError:
        print(f"😢 Invalid JSON in file: {filename}")
        return None

# 🎨 Display Functions

def show_report_summary(report):
    """Show a simple summary of the report."""
    print("\n" + "="*50)
    print("📊 YOUR COMPUTER REPORT 📊")
    print("="*50)
    print(f"Computer type: {report['computer']['type']}")
    print(f"Computer name: {report['computer']['name']}")
    print(f"System packages: {len(report['packages']['system'])}")
    print(f"App packages: {len(report['packages']['apps'])}")
    print(f"Total packages: {len(report['packages']['system']) + len(report['packages']['apps'])}")
    print("="*50)

def show_some_packages(report, count=5):
    """Show some of the packages."""
    print("\n📦 Some system packages:")
    for pkg in report['packages']['system'][:count]:
        print(f"  • {pkg}")
    
    print("\n🎮 Some app packages:")
    for pkg in report['packages']['apps'][:count]:
        print(f"  • {pkg}")

# ✅ Check Functions

def check_report_is_good(report):
    """Check if the report looks good."""
    if not isinstance(report, dict):
        return False, "Report is not a dictionary"
    
    if "computer" not in report:
        return False, "Missing computer info"
    
    if "packages" not in report:
        return False, "Missing packages info"
    
    if "system" not in report["packages"]:
        return False, "Missing system packages"
    
    if "apps" not in report["packages"]:
        return False, "Missing app packages"
    
    return True, "Report looks good!"
