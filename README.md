# 🚀 MIF Environment Mapper v1.0.0

A Python tool that maps and reports your computer's environment, packages, and installed applications. Perfect for understanding what's on your system!

## ✨ Features

- 🔍 **Automatic Detection** - Identifies your OS (Mac, Linux, Windows) and installs installed packages
- 📦 **Package Discovery** - Finds system packages and programming language packages (Python, Node.js, etc.)
- 🔒 **Privacy-First** - Automatically hides sensitive information like passwords and usernames
- 📊 **Detailed Reports** - Generates comprehensive JSON reports of your environment
- 💻 **Cross-Platform** - Works on macOS (Homebrew), Linux (apt, rpm, pacman), and more
- 🎯 **Easy Mode** - Simple guided interface perfect for beginners

## 📋 Requirements

- **Python 3.8+**
- Zero external dependencies (uses only Python standard library)
- No installation needed!

## 🚀 Quick Start

### Method 1: Easy Mode (Perfect for Beginners!)

```bash
python easy_main.py
```

Just answer the questions and the program does the rest!

### Method 2: Advanced Mode

```bash
python main.py
```

For more control over the mapping process.

### Method 3: Run Everything

```bash
python run.py
```

Complete system analysis with all checks.

## 📁 What's Inside

| File | Purpose |
|------|---------|
| `easy_main.py` | 🎯 Beginner-friendly version with guided questions |
| `main.py` | 🔧 Core mapping logic and package detection |
| `run.py` | 🏃 Complete system analyzer |
| `easy_tools.py` | 🛠️ Helper functions for easy mode |
| `verify_mif_compliance.py` | ✅ Checks environment compliance |
| `verify_easy_mode.py` | ✅ Tests easy mode functionality |
| `tests/` | 🧪 Unit tests for all components |

## 💡 How It Works

1. **Detects Your Computer**
   - Identifies OS type (Darwin/Mac, Linux, Windows)
   - Gets computer name and system info

2. **Finds Installed Packages**
   - System packages (via Homebrew, apt, rpm, pacman)
   - Programming language packages (Python, Node.js)

3. **Protects Your Privacy**
   - Hides user paths, passwords, and tokens
   - Uses `[HIDDEN]` placeholders for sensitive data

4. **Generates Report**
   - Creates detailed JSON file with all findings
   - Timestamps each report

## 📊 Example Output

```
🌟 MIF ENVIRONMENT MAPPER 🌟

Hi! 👋 I'll help you see what's on your computer.

==================================================
📊 YOUR COMPUTER REPORT 📊
==================================================
Computer type: darwin
Computer name: MacBook-Pro
System packages: 133
App packages: 87
==================================================

📦 Some system packages:
  • python@3.12 3.12.0
  • git 2.43.0
  • node 21.5.0

🎮 Some app packages:
  • numpy==1.26.2
  • pandas==2.1.4
```

## 📄 Report Format

The generated JSON report looks like this:

```json
{
  "computer": {
    "type": "darwin",
    "name": "MacBook-Pro",
    "time": "2026-06-07T22:14:48Z"
  },
  "packages": {
    "system": [
      "python@3.12 3.12.0",
      "git 2.43.0"
    ],
    "apps": [
      "numpy==1.26.2",
      "pandas==2.1.4"
    ]
  }
}
```

## 🔒 Privacy & Safety

✅ **Secure by Default**
- No internet connection required
- Nothing is uploaded anywhere
- Only reads package information
- Automatically masks sensitive data

✅ **What Gets Hidden**
- User home directory paths
- Password strings
- Authentication tokens
- API keys

## 🛠️ Troubleshooting

### Python not found?
```bash
python3 --version
```
Make sure Python 3.8+ is installed.

### Permission denied?
```bash
chmod +x easy_main.py
```

### Package detection not working?
- Make sure you have at least one package manager installed
- Check that the package manager is in your PATH
- Try running with explicit Python: `python3 easy_main.py`

## 🧪 Testing

Run the test suite:

```bash
python verify_easy_mode.py
python verify_mif_compliance.py
```

## 📖 Documentation

- **Easy Mode Guide**: See `README_EASY.md` for step-by-step instructions
- **Code Comments**: Check source files for detailed code documentation

## 🎓 Educational Value

Perfect for learning about:
- Environment variables and system configuration
- Package management on different OSes
- Data privacy and security
- JSON file formats
- Python system programming

## 👨‍💻 Made by

**David Nichols** - 17 years old developer

## 📝 License

MIT License - Feel free to use, modify, and share!

## 🎯 Version

**v1.0.0** - Initial Release

---

**Have fun exploring your computer!** 🎉

Need help? Check the troubleshooting section or review the output carefully!
