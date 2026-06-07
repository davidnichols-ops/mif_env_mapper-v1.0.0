#!/usr/bin/env python3
"""
🌟 MIF Environment Mapper - Easy Mode 🌟
Made for kids to use! Just follow the questions.
"""

import os
import sys
import platform
import subprocess
import json
from datetime import datetime

# Simple helper functions
def ask_yes_no(question):
    """Ask a yes/no question and get answer."""
    while True:
        answer = input(f"{question} (y/n): ").lower()
        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no']:
            return False
        print("Please type 'y' for yes or 'n' for no")

def run_command(cmd):
    """Run a command and get the output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout.strip().split('\n') if result.stdout else []
    except:
        return []

def hide_secrets(text):
    """Hide secret information like passwords and user names."""
    if not isinstance(text, str):
        return text
    
    # Hide user paths
    text = text.replace("/Users/", "/Users/[HIDDEN]")
    text = text.replace("/home/", "/home/[HIDDEN]")
    
    # Hide passwords
    if "password=" in text.lower():
        text = text.split("password=")[0] + "password=[HIDDEN]"
    
    # Hide tokens
    if "token=" in text.lower():
        text = text.split("token=")[0] + "token=[HIDDEN]"
    
    return text

def get_packages():
    """Get all the packages on your computer."""
    packages = {"system": [], "apps": []}
    
    # Check what kind of computer we have
    computer_type = platform.system().lower()
    
    if computer_type == "darwin":  # Mac
        print("🍎 Found a Mac! Checking Homebrew packages...")
        brew_pkgs = run_command(["brew", "list", "--versions"])
        packages["system"].extend(brew_pkgs)
        
    elif computer_type == "linux":  # Linux
        print("🐧 Found Linux! Checking packages...")
        # Try different package managers
        for cmd in [["dpkg-query", "-W", "-f=${Package} ${Version}\n"],
                   ["rpm", "-qa", "--queryformat", "%{NAME} %{VERSION}\n"],
                   ["pacman", "-Q"]]:
            result = run_command(cmd)
            if result:
                packages["system"].extend(result)
                break
    
    # Check for programming language packages
    print("📦 Checking for programming packages...")
    
    # Python packages
    pip_pkgs = run_command([sys.executable, "-m", "pip", "freeze"])
    packages["apps"].extend(pip_pkgs)
    
    # Node packages
    npm_pkgs = run_command(["npm", "list", "-g", "--depth=0", "--parseable"])
    packages["apps"].extend(npm_pkgs)
    
    return packages

def make_report(packages):
    """Make a nice report of all the packages."""
    report = {
        "computer": {
            "type": platform.system().lower(),
            "name": platform.node(),
            "time": datetime.now().isoformat()
        },
        "packages": {
            "system": [hide_secrets(p) for p in packages["system"]],
            "apps": [hide_secrets(p) for p in packages["apps"]]
        }
    }
    return report

def show_summary(report):
    """Show a simple summary."""
    print("\n" + "="*50)
    print("📊 YOUR COMPUTER REPORT 📊")
    print("="*50)
    print(f"Computer type: {report['computer']['type']}")
    print(f"Computer name: {report['computer']['name']}")
    print(f"System packages: {len(report['packages']['system'])}")
    print(f"App packages: {len(report['packages']['apps'])}")
    print("="*50)

def save_report(report, filename):
    """Save the report to a file."""
    with open(filename, 'w') as f:
        json.dump(report, f, indent=2)
    print(f"✅ Report saved to: {filename}")

def main():
    """Main program - easy to follow!"""
    print("\n" + "🌟"*25)
    print("🌟 MIF ENVIRONMENT MAPPER 🌟")
    print("🌟"*25)
    print("\nHi! 👋 I'll help you see what's on your computer.")
    print("Just answer a few simple questions!\n")
    
    # Step 1: What do you want to do?
    print("What would you like to do?")
    print("1. Just look at the packages (quick)")
    print("2. Save a report to a file")
    print("3. Both - look AND save")
    
    choice = input("\nType 1, 2, or 3: ")
    
    # Get the packages
    print("\n🔍 Looking at your computer...")
    packages = get_packages()
    report = make_report(packages)
    
    # Show the summary
    show_summary(report)
    
    # Save if they want
    if choice in ['2', '3']:
        filename = input("\nWhat should we name the file? (default: my_report.json): ")
        if not filename:
            filename = "my_report.json"
        if not filename.endswith('.json'):
            filename += '.json'
        save_report(report, filename)
    
    # Show some packages if they want
    if choice in ['1', '3']:
        show = ask_yes_no("\nDo you want to see some of the packages?")
        if show:
            print("\n📦 Some system packages:")
            for pkg in report['packages']['system'][:5]:
                print(f"  • {pkg}")
            
            print("\n🎮 Some app packages:")
            for pkg in report['packages']['apps'][:5]:
                print(f"  • {pkg}")
    
    print("\n" + "🎉"*25)
    print("🎉 All done! Great job! 🎉")
    print("🎉"*25 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bye! Thanks for playing!")
    except Exception as e:
        print(f"\n😢 Oops! Something went wrong: {e}")
        print("Don't worry, just try again!")
