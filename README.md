# CK3 DNA Duplicator

A simple desktop tool for duplicating Crusader Kings III character DNA strings.

### Before Continuing
Windows will think the executable is a threat, you can restore it in the Protection History. 

**This is normal**, since this executable doesn't have a certificate, if you're suspicious you can just build it yourself, though it will still detect it as a threat.

## How to use
1. Paste Ruler DNA in "Input DNA".
2. Click Process.
3. Click Copy Result.

## How to Run
1. Download `DNA Duplicator.exe` (To build it yourself, see below).
2. Double-click to launch.

## Building Your Own Executable

### Requirements
- Python 3.12
- All dependencies:
	```powershell
	pip install -r requirements.txt
	```
- Nuitka (for building):
	```powershell
	pip install nuitka
	```

### Build Command
```powershell
py -3.12 -m nuitka --onefile --lto=no --windows-console-mode=disable --windows-icon-from-ico=icon.ico --include-data-file=interface.html=interface.html --output-filename="DNA Duplicator.exe" dd_interface.py
```
This creates a portable `DNA Duplicator.exe`, you can move this anywhere you want.



## License
MIT License. See LICENSE file.

## Credits
- Deticaru (author)
- pywebview, Nuitka, pythonnet

---
For issues or suggestions, open an issue on GitHub or contact the author.
