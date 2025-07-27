# brute_force.py
import itertools
import zipfile
import rarfile
import pikepdf
import py7zr
import multiprocessing
import os
import logging

os.makedirs("logs", exist_ok=True)
logging.basicConfig(filename=f"logs/brute_{int(os.path.getmtime(__file__))}.log", level=logging.INFO)

# --- Try Password Functions ---
def try_zip_password(file_path, password):
    try:
        with zipfile.ZipFile(file_path) as zf:
            zf.extractall(pwd=password.encode())
        return True
    except:
        return False

def try_rar_password(file_path, password):
    try:
        rarfile.UNRAR_TOOL = "unRAR.exe"
        rf = rarfile.RarFile(file_path)
        rf.extractall(pwd=password)
        return True
    except:
        return False

def try_pdf_password(file_path, password):
    try:
        with pikepdf.open(file_path, password=password):
            return True
    except:
        return False

def try_7z_password(file_path, password):
    try:
        with py7zr.SevenZipFile(file_path, mode='r', password=password) as archive:
            archive.extractall()
        return True
    except:
        return False

def get_try_function(file_type):
    file_type = file_type.upper()
    return {
        "ZIP": try_zip_password,
        "RAR": try_rar_password,
        "PDF": try_pdf_password,
        "7Z": try_7z_password
    }.get(file_type)

# --- Worker Function ---
def brute_worker(file_path, combos, file_type, stop_event, found, counter, callback=None):
    try_func = get_try_function(file_type)
    for combo in combos:
        if stop_event.is_set(): return
        password = ''.join(combo)
        if try_func and try_func(file_path, password):
            found.append(password)
            stop_event.set()
            return
        with counter.get_lock():
            counter.value += 1
            if callback and counter.value % 100 == 0:
                callback(counter.value)

# --- Brute Force Main Entry ---
def threaded_brute_force(file_path, charset, max_len, file_type="ZIP", on_result=None, progress_callback=None):
    total = sum(len(charset) ** i for i in range(1, max_len + 1))
    manager = multiprocessing.Manager()
    stop_event = manager.Event()
    found = manager.list()
    counter = multiprocessing.Value('i', 0)
    num_cores = multiprocessing.cpu_count()

    for length in range(1, max_len + 1):
        combos = list(itertools.product(charset, repeat=length))
        chunk_size = len(combos) // num_cores
        processes = []
        for i in range(num_cores):
            chunk = combos[i*chunk_size:(i+1)*chunk_size]
            p = multiprocessing.Process(target=brute_worker,
                                        args=(file_path, chunk, file_type, stop_event, found, counter, progress_callback))
            processes.append(p)
            p.start()
        for p in processes:
            p.join()
        if stop_event.is_set(): break

    if found:
        logging.info(f"{file_type} Brute-force success: {found[0]}")
        if on_result:
            on_result(True, found[0])
        return found[0]
    else:
        logging.info(f"{file_type} Brute-force failed.")
        if on_result:
            on_result(False, None)
        return None
