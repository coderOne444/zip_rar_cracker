# ZIP & RAR Password Cracker
I made this for education purpose only and please don't use for any illegal/malicious activity

## Features
- Brute-force and dictionary attacks for ZIP and RAR files
- Multiprocessing for fast brute-force
- Progress bar and ETA display
- Pause, resume, and cancel attacks
- GUI with Tkinter
- Error handling and user feedback

## Requirements
- Python 3.7+
- See requirements.txt for dependencies

## Usage
1. Run `python gui_app.py` to launch the GUI.
2. Select a ZIP or RAR file and a wordlist, or use brute-force mode.
3. Use the progress bar, ETA, and control buttons during attacks.

## Notes
- For RAR files, ensure `unRAR.exe` is present in the project directory.
- For best brute-force speed, use a multi-core CPU.
