# gui_app.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import time
import os
import sys
import logging
from zip_rar_cracker import crack_file
from utils.brute_force import threaded_brute_force

# --- Logging Setup ---
os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=f"logs/session_{int(time.time())}.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# --- Helper Functions ---
def browse_file(entry):
    path = filedialog.askopenfilename()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def set_status(text, running=False):
    status_var.set(text)
    if running:
        start_timer()
        brute_button.config(state=tk.DISABLED)
        dict_button.config(state=tk.DISABLED)
    else:
        stop_timer()
        brute_button.config(state=tk.NORMAL)
        dict_button.config(state=tk.NORMAL)

def start_timer():
    timer_start[0] = time.time()
    timer_running[0] = True
    update_timer()

def stop_timer():
    timer_running[0] = False

def update_timer():
    if timer_running[0]:
        elapsed = int(time.time() - timer_start[0])
        timer_var.set(f"Elapsed: {elapsed}s")
        app.after(1000, update_timer)

# --- Dictionary Mode ---
def run_dictionary_attack():
    file_path = file_entry.get()
    wordlist_path = wordlist_entry.get()
    file_type = file_type_var.get()
    if not file_path or not wordlist_path:
        messagebox.showerror("Error", "Please select both the file and wordlist.")
        return

    with open(wordlist_path, 'r', encoding='latin-1') as f:
        passwords = f.read().splitlines()
    total = len(passwords)
    progress_total[0] = total
    progress_var.set(0)
    progress_bar.config(maximum=total)
    eta_var.set("ETA: --")
    attack_control['pause'] = False
    attack_control['cancel'] = False

    def progress_callback(count):
        if attack_control['cancel']:
            sys.exit(0)
        while attack_control['pause']:
            time.sleep(0.1)
        elapsed = time.time() - start_time[0]
        if count:
            eta = int((elapsed / count) * (progress_total[0] - count))
            eta_var.set(f"ETA: {eta}s")
        app.after(0, lambda: progress_var.set(count))
        app.after(0, lambda: progress_bar.config(value=count))

    def on_result(success, password):
        set_status("Done", running=False)
        progress_bar.config(value=progress_total[0])
        eta_var.set("ETA: --")
        if success:
            messagebox.showinfo("Success", f"Password found: {password}")
            logging.info(f"Password cracked: {password}")
        else:
            messagebox.showerror("Failed", "Password not found.")
            logging.info("Password not found.")

    def worker():
        set_status(f"Running {file_type} dictionary attack...", running=True)
        success, result = crack_file(file_path, wordlist_path, file_type, progress_callback)
        on_result(success, result)

    start_time[0] = time.time()
    threading.Thread(target=worker, daemon=True).start()

# --- Brute-force Mode ---
def run_brute_force():
    file_path = brute_file_entry.get()
    charset = charset_entry.get()
    try:
        max_len = int(maxlen_entry.get())
    except:
        messagebox.showerror("Error", "Invalid max length.")
        return
    if not file_path or not charset or max_len < 1:
        messagebox.showerror("Error", "All fields are required.")
        return

    total = sum(len(charset) ** l for l in range(1, max_len + 1))
    progress_total[0] = total
    progress_var.set(0)
    progress_bar.config(maximum=total)
    eta_var.set("ETA: --")
    attack_control['pause'] = False
    attack_control['cancel'] = False

    def progress_callback(count):
        if attack_control['cancel']:
            sys.exit(0)
        while attack_control['pause']:
            time.sleep(0.1)
        elapsed = time.time() - start_time[0]
        if count:
            eta = int((elapsed / count) * (progress_total[0] - count))
            eta_var.set(f"ETA: {eta}s")
        app.after(0, lambda: progress_var.set(count))
        app.after(0, lambda: progress_bar.config(value=count))

    def on_result(success, password):
        set_status("Done", running=False)
        progress_bar.config(value=progress_total[0])
        eta_var.set("ETA: --")
        if success:
            messagebox.showinfo("Success", f"Password found: {password}")
            logging.info(f"Brute-force cracked password: {password}")
        else:
            messagebox.showerror("Failed", "Password not found.")
            logging.info("Brute-force failed.")

    def worker():
        set_status("Brute-forcing...", running=True)
        file_type = file_type_var.get()
        threaded_brute_force(file_path, charset, max_len, file_type=file_type,
                             on_result=on_result, progress_callback=progress_callback)

    start_time[0] = time.time()
    threading.Thread(target=worker, daemon=True).start()

# --- GUI Setup ---
app = tk.Tk()
app.title("Password Cracker")
app.geometry("520x500")
app.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", background="#1e1e1e", foreground="white")
style.configure("TButton", background="#333", foreground="white")

file_types = ["ZIP", "RAR", "PDF", "OFFICE", "7Z"]
file_type_var = tk.StringVar(value="ZIP")
progress_var = tk.DoubleVar(value=0)
eta_var = tk.StringVar(value="ETA: --")
status_var = tk.StringVar(value="Idle")
timer_var = tk.StringVar(value="Elapsed: 0s")
progress_total = [1]
attack_control = {'pause': False, 'cancel': False}
timer_running = [False]
timer_start = [0]

ttk.Label(app, text="File to Crack").pack()
file_entry = tk.Entry(app, width=60)
file_entry.pack()
ttk.Button(app, text="Browse File", command=lambda: browse_file(file_entry)).pack()

ttk.Label(app, text="Wordlist File").pack()
wordlist_entry = tk.Entry(app, width=60)
wordlist_entry.pack()
ttk.Button(app, text="Browse Wordlist", command=lambda: browse_file(wordlist_entry)).pack()

ttk.Label(app, text="File Type").pack()
ttk.Combobox(app, textvariable=file_type_var, values=file_types).pack()

dict_button = ttk.Button(app, text="Start Dictionary Attack", command=run_dictionary_attack)
dict_button.pack(pady=10)

# --- Brute-force Section ---
ttk.Label(app, text="Brute-force File").pack()
brute_file_entry = tk.Entry(app, width=60)
brute_file_entry.pack()
ttk.Button(app, text="Browse", command=lambda: browse_file(brute_file_entry)).pack()

ttk.Label(app, text="Charset (e.g. abc123)").pack()
charset_entry = tk.Entry(app, width=50)
charset_entry.pack()

ttk.Label(app, text="Max Password Length").pack()
maxlen_entry = tk.Entry(app, width=5)
maxlen_entry.pack()

brute_button = ttk.Button(app, text="Start Brute-force", command=run_brute_force)
brute_button.pack(pady=10)

# --- Status ---
progress_bar = ttk.Progressbar(app, variable=progress_var, maximum=1, length=400)
progress_bar.pack(pady=5)
ttk.Label(app, textvariable=eta_var).pack()
ttk.Label(app, textvariable=status_var).pack()
ttk.Label(app, textvariable=timer_var).pack()

control_frame = ttk.Frame(app)
control_frame.pack(pady=5)
ttk.Button(control_frame, text="Pause", command=lambda: attack_control.update({'pause': True})).pack(side=tk.LEFT, padx=5)
ttk.Button(control_frame, text="Resume", command=lambda: attack_control.update({'pause': False})).pack(side=tk.LEFT, padx=5)
ttk.Button(control_frame, text="Cancel", command=lambda: attack_control.update({'cancel': True})).pack(side=tk.LEFT, padx=5)

app.mainloop()
