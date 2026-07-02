#!/usr/bin/env python3
"""
🚀 MIF Environment Mapper - Launcher
Choose your mode: Easy (for kids) or Main (for advanced users)
"""

import os
import sys
import json

PREFERENCE_FILE = ".mif_preference.json"

def get_preference():
    """Get saved preference, or None if not set."""
    if os.path.exists(PREFERENCE_FILE):
        try:
            with open(PREFERENCE_FILE, 'r') as f:
                data = json.load(f)
                return data.get('mode')
        except (json.JSONDecodeError, IOError, OSError):
            return None
    return None

def save_preference(mode):
    """Save user's preference."""
    with open(PREFERENCE_FILE, 'w') as f:
        json.dump({'mode': mode}, f)

def ask_mode():
    """Ask user which mode they want to use."""
    print("\n" + "="*60)
    print("🌟 WELCOME TO MIF ENVIRONMENT MAPPER 🌟")
    print("="*60)
    print("\nWhich mode would you like to use?\n")
    print("1. 🎈 EASY MODE - Simple and fun (great for kids!)")
    print("   - Wizard-style questions")
    print("   - Colorful with emojis")
    print("   - Very simple to understand")
    print()
    print("2. 🔧 MAIN MODE - Advanced (for developers)")
    print("   - Command-line interface")
    print("   - More options and features")
    print("   - Professional output")
    print()
    
    while True:
        choice = input("Type 1 for Easy or 2 for Main: ").strip()
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'main'
        print("Please type 1 or 2")

def run_easy_mode():
    """Run the easy mode."""
    print("\n🎈 Starting Easy Mode...\n")
    import easy_main
    easy_main.main()

def run_main_mode():
    """Run the main mode."""
    print("\n🔧 Starting Main Mode...\n")
    # Import and run the main CLI
    from mif_env_mapper.orchestrator import Orchestrator, OrchestrationError
    from mif_env_mapper.reporter import Reporter
    import argparse
    
    parser = argparse.ArgumentParser(
        prog="mif_env_mapper",
        description="Multi-Platform System Environment Mapping Engine"
    )
    
    parser.add_argument("--output", "-o", type=str, default=None, help="Output file path")
    parser.add_argument("--summary", "-s", action="store_true", help="Output summary")
    parser.add_argument("--compact", "-c", action="store_true", help="Compact JSON")
    parser.add_argument("--verify", "-v", action="store_true", help="Verification mode")
    parser.add_argument("--timeout", "-t", type=int, default=30, help="Timeout in seconds")
    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")
    
    args = parser.parse_args()
    
    try:
        orchestrator = Orchestrator(timeout=args.timeout, pretty_output=not args.compact)
        reporter = Reporter(pretty=not args.compact)
        
        if args.verify:
            print("[MIF] Running verification mode...")
            data = orchestrator.run_silent()
            print(f"[MIF] Verification successful!")
            print(f"[MIF] Platform: {data['system_metadata']['os_platform']}")
            print(f"[MIF] System packages: {len(data['packages']['system_level'])}")
            print(f"[MIF] Runtime packages: {len(data['packages']['language_runtimes'])}")
            print(f"[MIF] Duration: {orchestrator.duration_ms}ms")
            return 0
        
        data = orchestrator.run_silent()
        
        if args.output:
            with open(args.output, "w") as output_target:
                if args.summary:
                    reporter.write_summary(data, output_target)
                else:
                    reporter.write_json(data, output_target)
            print(f"[MIF] Output written to: {args.output}")
        else:
            if args.summary:
                reporter.write_summary(data, None)
            else:
                reporter.write_json(data, None)
        
        return 0
        
    except OrchestrationError as e:
        print(f"CRITICAL_PIPELINE_ERROR: {str(e)}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\n[MIF] Operation cancelled by user", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"UNEXPECTED_ERROR: {str(e)}", file=sys.stderr)
        return 2

def ask_to_change_preference():
    """Ask if user wants to change their preference."""
    print("\n" + "="*60)
    choice = input("Would you like to change your mode choice? (y/n): ").lower()
    return choice in ['y', 'yes']

def main():
    """Main launcher."""
    # Check if preference exists
    preference = get_preference()
    
    if preference is None:
        # First run - ask for preference
        mode = ask_mode()
        save_preference(mode)
        print(f"\n✅ Saved your choice! Next time we'll remember it.\n")
    else:
        # Preference exists - ask if they want to change it
        print(f"\n📋 Your saved preference: {preference.upper()} MODE")
        
        if ask_to_change_preference():
            mode = ask_mode()
            save_preference(mode)
            print(f"\n✅ Updated your choice!\n")
        else:
            mode = preference
            print(f"\n✅ Using your saved choice: {mode.upper()} MODE\n")
    
    # Run the chosen mode
    if mode == 'easy':
        run_easy_mode()
    else:
        sys.exit(run_main_mode())

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Bye! Thanks for using MIF Environment Mapper!")
    except Exception as e:
        print(f"\n😢 Oops! Something went wrong: {e}")
        print("Please try again or ask for help.")
