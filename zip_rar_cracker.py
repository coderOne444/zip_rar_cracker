import zipfile
import rarfile
import os
from tqdm import tqdm
from tkinter import filedialog, Tk
from utils.brute_force import threaded_brute_force
import pikepdf
import msoffcrypto
import py7zr

def crack_zip(zip_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(zip_path):
        return False, f"ZIP file not found: {zip_path}"
    if not os.path.isfile(wordlist_path):
        return False, f"Wordlist file not found: {wordlist_path}"
    try:
        with zipfile.ZipFile(zip_path) as zf:
            with open(wordlist_path, 'r', encoding='latin-1') as f:
                passwords = f.read().splitlines()
                for i, pwd in enumerate(passwords):
                    try:
                        zf.extractall(pwd=pwd.encode())
                        if progress_callback:
                            progress_callback(i + 1)
                        return True, pwd
                    except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile):
                        if progress_callback:
                            progress_callback(i + 1)
                        continue
        return False, "Password not found in wordlist."
    except Exception as e:
        return False, f"ZIP Error: {e}"

def crack_rar(rar_path, wordlist_path, unrar_tool_path="unRAR.exe", progress_callback=None):
    if not os.path.isfile(rar_path):
        return False, f"RAR file not found: {rar_path}"
    if not os.path.isfile(wordlist_path):
        return False, f"Wordlist file not found: {wordlist_path}"
    try:
        rarfile.UNRAR_TOOL = unrar_tool_path
        rf = rarfile.RarFile(rar_path)
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            passwords = f.read().splitlines()
            for i, pwd in enumerate(passwords):
                try:
                    rf.extractall(pwd=pwd)
                    if progress_callback:
                        progress_callback(i + 1)
                    return True, pwd
                except (rarfile.BadRarFile, rarfile.RarWrongPassword, RuntimeError):
                    if progress_callback:
                        progress_callback(i + 1)
                    continue
        return False, "Password not found in wordlist."
    except Exception as e:
        return False, f"RAR Error: {e}"

def crack_pdf(pdf_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(pdf_path):
        return False, f"PDF file not found: {pdf_path}"
    if not os.path.isfile(wordlist_path):
        return False, f"Wordlist file not found: {wordlist_path}"
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            passwords = f.read().splitlines()
            for i, pwd in enumerate(passwords):
                try:
                    with pikepdf.open(pdf_path, password=pwd):
                        if progress_callback:
                            progress_callback(i + 1)
                        return True, pwd
                except pikepdf._qpdf.PasswordError:
                    if progress_callback:
                        progress_callback(i + 1)
                    continue
        return False, "Password not found in wordlist."
    except Exception as e:
        return False, f"PDF Error: {e}"

def crack_office(office_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(office_path):
        return False, f"Office file not found: {office_path}"
    if not os.path.isfile(wordlist_path):
        return False, f"Wordlist file not found: {wordlist_path}"
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            passwords = f.read().splitlines()
            for i, pwd in enumerate(passwords):
                try:
                    with open(office_path, 'rb') as docf:
                        office = msoffcrypto.OfficeFile(docf)
                        office.load_key(password=pwd)
                        office.decrypt(None)  # Will raise if wrong
                        if progress_callback:
                            progress_callback(i + 1)
                        return True, pwd
                except Exception:
                    if progress_callback:
                        progress_callback(i + 1)
                    continue
        return False, "Password not found in wordlist."
    except Exception as e:
        return False, f"Office Error: {e}"

def crack_7z(sevenz_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(sevenz_path):
        return False, f"7z file not found: {sevenz_path}"
    if not os.path.isfile(wordlist_path):
        return False, f"Wordlist file not found: {wordlist_path}"
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            passwords = f.read().splitlines()
            for i, pwd in enumerate(passwords):
                try:
                    with py7zr.SevenZipFile(sevenz_path, mode='r', password=pwd) as archive:
                        archive.extractall()
                        if progress_callback:
                            progress_callback(i + 1)
                        return True, pwd
                except Exception:
                    if progress_callback:
                        progress_callback(i + 1)
                    continue
        return False, "Password not found in wordlist."
    except Exception as e:
        return False, f"7z Error: {e}"

def crack_file(file_path, wordlist_path, file_type, progress_callback=None):
    if file_type == 'ZIP':
        return crack_zip(file_path, wordlist_path, progress_callback=progress_callback)
    elif file_type == 'RAR':
        return crack_rar(file_path, wordlist_path, progress_callback=progress_callback)
    elif file_type == 'PDF':
        return crack_pdf(file_path, wordlist_path, progress_callback=progress_callback)
    elif file_type == 'OFFICE':
        return crack_office(file_path, wordlist_path, progress_callback=progress_callback)
    elif file_type == '7Z':
        return crack_7z(file_path, wordlist_path, progress_callback=progress_callback)
    else:
        return False, f"Unsupported file type: {file_type}"

def browse_file():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename()

def main():
    print("🔐 Welcome to ZIP & RAR Password Cracker")
    choice = input("Select mode:\n1. ZIP\n2. RAR\n3. Brute Force ZIP\nEnter choice: ")

    if choice == '1':
        zip_path = browse_file()
        wordlist = browse_file()
        success, result = crack_zip(zip_path, wordlist)
        if success:
            print(f"✅ ZIP Password found: {result}")
        else:
            print(f"❌ {result}")

    elif choice == '2':
        rar_path = browse_file()
        wordlist = browse_file()
        success, result = crack_rar(rar_path, wordlist)
        if success:
            print(f"✅ RAR Password found: {result}")
        else:
            print(f"❌ {result}")

    elif choice == '3':
        zip_path = browse_file()
        charset = input("Enter charset (e.g. abc123): ")
        try:
            max_len = int(input("Max password length: "))
        except ValueError:
            print("❌ Max length must be a number.")
            return
        threaded_brute_force(zip_path, charset, max_len)

    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
