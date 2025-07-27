import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from zip_rar_cracker import crack_zip, crack_rar, crack_file
from utils.brute_force import threaded_brute_force
import threading
import os
import time
import sys

def browse_file(entry):
    path = filedialog.askopenfilename()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def run_crack():
    file_path = file_entry.get()
    wordlist_path = wordlist_entry.get()
    file_type = file_type_var.get()

    if not file_path or not wordlist_path:
        messagebox.showerror("Error", "Please select both the file and the wordlist.")
        return
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"File not found: {file_path}")
        return
    if not os.path.isfile(wordlist_path):
        messagebox.showerror("Error", f"Wordlist not found: {wordlist_path}")
        return

    # Calculate total passwords
    with open(wordlist_path, 'r', encoding='latin-1') as f:
        passwords = f.read().splitlines()
    total = len(passwords)
    progress_total[0] = total
    progress_var.set(0)
    if progress_bar:
        progress_bar.config(maximum=total, value=0)
    eta_var.set("ETA: --")
    attack_control['pause'] = False
    attack_control['cancel'] = False

    def on_result(success, password):
        set_status("Done.", running=False)
        if success:
            messagebox.showinfo("Success", f"Password found: {password}")
        else:
            messagebox.showerror("Failed", "Password not found.")
        if progress_bar:
            progress_bar.config(value=progress_total[0])
        eta_var.set("ETA: --")

    start_time = [time.time()]

    def progress_callback(count):
        if attack_control['cancel']:
            sys.exit(0)
        while attack_control['pause']:
            time.sleep(0.1)
        elapsed = time.time() - start_time[0]
        if count > 0:
            eta = int((elapsed / count) * (progress_total[0] - count))
            eta_var.set(f"ETA: {eta}s")
        else:
            eta_var.set("ETA: --")
        app.after(0, lambda: progress_var.set(count))
        if progress_bar:
            app.after(0, lambda: progress_bar.config(value=count))

    def worker():
        set_status(f"Running {file_type} dictionary attack...", running=True)
        success, result = crack_file(file_path, wordlist_path, file_type, progress_callback=progress_callback)
        set_status("Done.", running=False)
        if success:
            messagebox.showinfo("Success", f"Password found: {result}")
        else:
            messagebox.showerror("Failed", result)
    threading.Thread(target=worker, daemon=True).start()

progress_var = tk.DoubleVar(value=0)
progress_bar = None
progress_total = [1]

# --- Pause/Resume/Cancel ---
attack_control = {'pause': False, 'cancel': False}
eta_var = tk.StringVar(value="ETA: --")

def run_brute_force():
    file_path = brute_file_entry.get()
    charset = charset_entry.get()
    try:
        max_len = int(maxlen_entry.get())
    except:
        messagebox.showerror("Error", "Max length must be a number.")
        return
    if not file_path or not charset:
        messagebox.showerror("Error", "Please select a file and enter a charset.")
        return
    if not os.path.isfile(file_path):
        messagebox.showerror("Error", f"File not found: {file_path}")
        return
    if max_len < 1:
        messagebox.showerror("Error", "Max length must be at least 1.")
        return

    total = sum(len(charset) ** l for l in range(1, max_len + 1))
    progress_total[0] = total
    progress_var.set(0)
    if progress_bar:
        progress_bar.config(maximum=total, value=0)
    eta_var.set("ETA: --")
    attack_control['pause'] = False
    attack_control['cancel'] = False

    def on_result(success, password):
        set_status("Done.", running=False)
        if success:
            messagebox.showinfo("Success", f"Password found: {password}")
        else:
            messagebox.showerror("Failed", "Password not found.")
        if progress_bar:
            progress_bar.config(value=progress_total[0])
        eta_var.set("ETA: --")

    start_time = [time.time()]

    def progress_callback(count):
        if attack_control['cancel']:
            sys.exit(0)
        while attack_control['pause']:
            time.sleep(0.1)
        elapsed = time.time() - start_time[0]
        if count > 0:
            eta = int((elapsed / count) * (progress_total[0] - count))
            eta_var.set(f"ETA: {eta}s")
        else:
            eta_var.set("ETA: --")
        app.after(0, lambda: progress_var.set(count))
        if progress_bar:
            app.after(0, lambda: progress_bar.config(value=count))

    def worker():
        set_status("Brute-forcing...", running=True)
        threaded_brute_force(file_path, charset, max_len, on_result=on_result, progress_callback=progress_callback)

    threading.Thread(target=worker, daemon=True).start()

# --- GUI Setup ---
app = tk.Tk()
app.title("ZIP & RAR Password Cracker")
app.geometry("500x440")
app.configure(bg="#1e1e1e")

# ✅ Now safe to declare these
status_var = tk.StringVar(value="Idle.")
timer_var = tk.StringVar(value="Elapsed: 0s")
timer_running = [False]
timer_start = [0]

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
    else:
        elapsed = int(time.time() - timer_start[0])
        timer_var.set(f"Elapsed: {elapsed}s")

# Style
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", background="#333", foreground="white")
style.configure("TLabel", background="#1e1e1e", foreground="white")

file_type_var = tk.StringVar(value="ZIP")
file_types = ["ZIP", "RAR", "PDF", "OFFICE", "7Z"]

# File + Wordlist
ttk.Label(app, text="File to Crack").pack()
file_entry = tk.Entry(app, width=50)
file_entry.pack(pady=5)
ttk.Button(app, text="Browse File", command=lambda: browse_file(file_entry)).pack()

ttk.Label(app, text="Wordlist File").pack()
wordlist_entry = tk.Entry(app, width=50)
wordlist_entry.pack(pady=5)
ttk.Button(app, text="Browse Wordlist", command=lambda: browse_file(wordlist_entry)).pack()

ttk.Label(app, text="Select File Type").pack()
ttk.Combobox(app, textvariable=file_type_var, values=file_types).pack(pady=5)

dict_button = ttk.Button(app, text="Start Dictionary Attack", command=run_crack)
dict_button.pack(pady=10)

# Brute-force
# Show/hide brute-force section based on file type
brute_section_widgets = []
def update_brute_section(*args):
    if file_type_var.get() == "ZIP":
        for w in brute_section_widgets:
            w.pack()
    else:
        for w in brute_section_widgets:
            w.pack_forget()
file_type_var.trace_add('write', update_brute_section)

brute_label = ttk.Label(app, text="Brute-force ZIP")
brute_label.pack(pady=10)
brute_section_widgets.append(brute_label)
brute_file_entry = tk.Entry(app, width=50)
brute_file_entry.pack(pady=5)
brute_section_widgets.append(brute_file_entry)
brute_browse = ttk.Button(app, text="Browse ZIP", command=lambda: browse_file(brute_file_entry))
brute_browse.pack()
brute_section_widgets.append(brute_browse)
charset_label = ttk.Label(app, text="Charset (e.g. abc123)")
charset_label.pack()
brute_section_widgets.append(charset_label)
charset_entry = tk.Entry(app, width=50)
charset_entry.pack(pady=5)
brute_section_widgets.append(charset_entry)
maxlen_label = ttk.Label(app, text="Max Password Length")
maxlen_label.pack()
brute_section_widgets.append(maxlen_label)
maxlen_entry = tk.Entry(app, width=5)
maxlen_entry.pack(pady=5)
brute_section_widgets.append(maxlen_entry)
brute_button = ttk.Button(app, text="Start Brute-force", command=run_brute_force)
brute_button.pack(pady=10)
brute_section_widgets.append(brute_button)
update_brute_section()

# Status and Timer
status_label = ttk.Label(app, textvariable=status_var, font=("Arial", 10, "italic"))
status_label.pack(pady=2)
timer_label = ttk.Label(app, textvariable=timer_var, font=("Arial", 10, "italic"))
timer_label.pack(pady=2)

# Add Progress Bar, ETA, and Pause/Resume/Cancel Buttons to GUI
progress_bar = ttk.Progressbar(app, variable=progress_var, maximum=1, length=400)
progress_bar.pack(pady=5)
eta_label = ttk.Label(app, textvariable=eta_var, font=("Arial", 10, "italic"))
eta_label.pack(pady=2)

button_frame = ttk.Frame(app)
button_frame.pack(pady=2)
pause_button = ttk.Button(button_frame, text="Pause", command=lambda: attack_control.update({'pause': True}))
pause_button.pack(side=tk.LEFT, padx=2)
resume_button = ttk.Button(button_frame, text="Resume", command=lambda: attack_control.update({'pause': False}))
resume_button.pack(side=tk.LEFT, padx=2)
cancel_button = ttk.Button(button_frame, text="Cancel", command=lambda: attack_control.update({'cancel': True}))
cancel_button.pack(side=tk.LEFT, padx=2)

app.mainloop()
