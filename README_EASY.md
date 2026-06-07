# 🌟 MIF Environment Mapper - Easy Mode 🌟

## What is this? 🤔

This program helps you see what's installed on your computer! It looks at all the packages and programs and makes a nice report.

## How to Use It 🚀

### Step 1: Open Terminal
- On Mac: Press `Command + Space`, type "Terminal", press Enter
- On Linux: Press `Ctrl + Alt + T`

### Step 2: Go to the Folder
```bash
cd /Users/david/CascadeProjects/mif_env_mapper
```

### Step 3: Run the Program
```bash
python easy_main.py
```

### Step 4: Answer the Questions
The program will ask you simple questions. Just type what it asks for!

- **Question 1:** What do you want to do?
  - Type `1` to just look at packages
  - Type `2` to save a report to a file
  - Type `3` to do both!

- **Question 2:** (if you chose 2 or 3) What should we name the file?
  - Just type a name like `my_report` or `computer_stuff`
  - It will add `.json` automatically

- **Question 3:** (if you chose 1 or 3) Do you want to see some packages?
  - Type `y` for yes
  - Type `n` for no

## What the Program Does 📋

1. **Finds your computer type** - Mac or Linux
2. **Looks for packages** - All the programs installed
3. **Hides secrets** - Keeps your passwords and names safe
4. **Makes a report** - Shows you what it found
5. **Saves the file** - (if you want) Keeps a copy

## Example Output 📊

```
🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟
🌟 MIF ENVIRONMENT MAPPER 🌟
🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟🌟

Hi! 👋 I'll help you see what's on your computer.
Just answer a few simple questions!

What would you like to do?
1. Just look at the packages (quick)
2. Save a report to a file
3. Both - look AND save

Type 1, 2, or 3: 3

🔍 Looking at your computer...
🍎 Found a Mac! Checking Homebrew packages...
📦 Checking for programming packages...

==================================================
📊 YOUR COMPUTER REPORT 📊
==================================================
Computer type: darwin
Computer name: Davids-MacBook-Pro
System packages: 133
App packages: 87
Total packages: 220
==================================================

What should we name the file? (default: my_report.json): my_stuff

✅ Report saved to: my_stuff.json

Do you want to see some of the packages? (y/n): y

📦 Some system packages:
  • python@3.12 3.12.0
  • git 2.43.0
  • node 21.5.0

🎮 Some app packages:
  • numpy==1.26.2
  • pandas==2.1.4
  • requests==2.31.0

🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
🎉 All done! Great job! 🎉
🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉
```

## What's in the Report File? 📄

The report file (JSON) looks like this:

```json
{
  "computer": {
    "type": "darwin",
    "name": "Davids-MacBook-Pro",
    "kernel": "23.1.0",
    "machine": "arm64",
    "time": "2026-06-07T17:00:00"
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

## Safety Features 🔒

- **Secrets are hidden** - Your passwords and usernames are replaced with `[HIDDEN]`
- **No internet needed** - Everything happens on your computer
- **Safe to run** - Only looks at packages, doesn't change anything

## Troubleshooting 🛠️

### "Command not found"
- Make sure you're in the right folder
- Check that Python is installed: `python --version`

### "Permission denied"
- You might need to run: `chmod +x easy_main.py`

### "Too slow"
- Some computers take longer to check packages
- Just wait a bit longer!

## Fun Facts! 🎓

- **System packages** = Programs that come with your computer (like Python, Git)
- **App packages** = Programs you installed for coding (like numpy, pandas)
- **JSON** = A simple way to store information in a file

## Need Help? 🆘

If something doesn't work:
1. Read the error message carefully
2. Try running the program again
3. Ask an adult for help if you're stuck

## Made For Kids! 👶

This program is designed to be:
- ✅ Easy to understand
- ✅ Fun to use
- ✅ Safe
- ✅ Educational

Have fun exploring your computer! 🎉
