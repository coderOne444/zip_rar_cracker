# 🔐 ZIP & RAR Password Cracker 
For Education purpose only !!

![License](https://img.shields.io/github/license/coderOne444/zip_rar_cracker?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square)
![Status](https://img.shields.io/badge/status-active-success?style=flat-square)

A powerful, multi-format password recovery tool for ZIP, RAR, PDF, Office, and 7Z files.  
Supports both **dictionary attacks** and **brute-force attacks**, with a full **GUI** and **Flask Web UI**.

---

## ✨ Features

✅ Supports file formats: `ZIP`, `RAR`, `PDF`, `OFFICE`, `7Z`  
✅ Brute-force and dictionary attack modes  
✅ Multi-core brute-force using `multiprocessing`  
✅ Real-time GUI with pause/resume/cancel controls  
✅ Flask-based web UI for online use  
✅ Logging system and ETA tracking  
✅ EXE packaging and installer ready  
✅ Dark-themed Tkinter GUI

---

## 🖼️ GUI Preview

> *(You can add a screenshot here if you like)*

```bash
python gui_app.py
```

![Screenshot](images/preview.png)

---

## 🌐 Web Version

Launch Flask server:
```bash
cd web_app
python app.py
```

Visit: http://localhost:5000

---

## 🛠️ Tech Stack

- `Python 3.8+`
- `tkinter` (GUI)
- `flask` (Web UI)
- `rarfile`, `pikepdf`, `py7zr`, `msoffcrypto`
- `multiprocessing`, `threading`, `logging`

---

## 📦 Installation

### 🔁 Clone the repo:
```bash
git clone https://github.com/coderOne444/zip_rar_cracker.git
cd zip_rar_cracker
```

### 📦 Install dependencies:
```bash
pip install -r requirements.txt
```

> Make sure `unRAR.exe` is present in the root for RAR support (Windows only).

---

## 🚀 Usage

### GUI (Desktop):
```bash
python gui_app.py
```

### Web (Browser):
```bash
cd web_app
python app.py
```

---

## 🔧 Packaging to EXE (Optional)

```bash
pyinstaller --onefile --noconsole gui_app.py
```

Installer script available in `installer_script.iss` (Inno Setup).

---

## 📁 Folder Structure

```
zip_rar_cracker/
├── gui_app.py
├── zip_rar_cracker.py
├── brute_force.py
├── requirements.txt
├── logs/
├── web_app/
│   ├── app.py
│   └── templates/index.html
├── installer_script.iss
├── password_cracker.spec
└── README.md
```

---

## 🧠 Contributing

Pull requests welcome! Feel free to open issues or feature requests.

---

## 📜 License

MIT License — See `LICENSE` file for details.

---

## 🔗 Connect With Me

📧 [Email Me](mailto:you@example.com)  
🔗 [LinkedIn](https://www.linkedin.com/in/yourprofile)  
🐙 [GitHub](https://github.com/coderOne444)

---

> 🚨 For educational and legal recovery use only. Do **not** use on unauthorized systems.
