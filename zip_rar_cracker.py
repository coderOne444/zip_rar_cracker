# zip_rar_cracker.py
import os
import zipfile
import rarfile
import pikepdf
import msoffcrypto
import py7zr
import logging

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def crack_zip(file_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(file_path): return False, "ZIP file not found"
    try:
        with zipfile.ZipFile(file_path) as zf, open(wordlist_path, 'r', encoding='latin-1') as f:
            for i, pwd in enumerate(f.read().splitlines()):
                try:
                    zf.extractall(pwd=pwd.encode())
                    if progress_callback: progress_callback(i + 1)
                    logger.info(f"ZIP Password found: {pwd}")
                    return True, pwd
                except:
                    if progress_callback: progress_callback(i + 1)
        return False, "Password not found in wordlist."
    except Exception as e:
        logger.error(f"ZIP Error: {e}")
        return False, str(e)

def crack_rar(file_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(file_path): return False, "RAR file not found"
    try:
        rarfile.UNRAR_TOOL = "unRAR.exe"
        rf = rarfile.RarFile(file_path)
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            for i, pwd in enumerate(f.read().splitlines()):
                try:
                    rf.extractall(pwd=pwd)
                    if progress_callback: progress_callback(i + 1)
                    logger.info(f"RAR Password found: {pwd}")
                    return True, pwd
                except:
                    if progress_callback: progress_callback(i + 1)
        return False, "Password not found in wordlist."
    except Exception as e:
        logger.error(f"RAR Error: {e}")
        return False, str(e)

def crack_pdf(file_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(file_path): return False, "PDF file not found"
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            for i, pwd in enumerate(f.read().splitlines()):
                try:
                    with pikepdf.open(file_path, password=pwd):
                        if progress_callback: progress_callback(i + 1)
                        logger.info(f"PDF Password found: {pwd}")
                        return True, pwd
                except:
                    if progress_callback: progress_callback(i + 1)
        return False, "Password not found in wordlist."
    except Exception as e:
        logger.error(f"PDF Error: {e}")
        return False, str(e)

def crack_office(file_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(file_path): return False, "Office file not found"
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            for i, pwd in enumerate(f.read().splitlines()):
                try:
                    with open(file_path, 'rb') as doc:
                        office = msoffcrypto.OfficeFile(doc)
                        office.load_key(password=pwd)
                        office.decrypt(None)
                        if progress_callback: progress_callback(i + 1)
                        logger.info(f"Office Password found: {pwd}")
                        return True, pwd
                except:
                    if progress_callback: progress_callback(i + 1)
        return False, "Password not found in wordlist."
    except Exception as e:
        logger.error(f"Office Error: {e}")
        return False, str(e)

def crack_7z(file_path, wordlist_path, progress_callback=None):
    if not os.path.isfile(file_path): return False, "7Z file not found"
    try:
        with open(wordlist_path, 'r', encoding='latin-1') as f:
            for i, pwd in enumerate(f.read().splitlines()):
                try:
                    with py7zr.SevenZipFile(file_path, mode='r', password=pwd) as archive:
                        archive.extractall()
                        if progress_callback: progress_callback(i + 1)
                        logger.info(f"7Z Password found: {pwd}")
                        return True, pwd
                except:
                    if progress_callback: progress_callback(i + 1)
        return False, "Password not found in wordlist."
    except Exception as e:
        logger.error(f"7Z Error: {e}")
        return False, str(e)

def crack_file(file_path, wordlist_path, file_type, progress_callback=None):
    file_type = file_type.upper()
    if file_type == 'ZIP':
        return crack_zip(file_path, wordlist_path, progress_callback)
    elif file_type == 'RAR':
        return crack_rar(file_path, wordlist_path, progress_callback)
    elif file_type == 'PDF':
        return crack_pdf(file_path, wordlist_path, progress_callback)
    elif file_type == 'OFFICE':
        return crack_office(file_path, wordlist_path, progress_callback)
    elif file_type == '7Z':
        return crack_7z(file_path, wordlist_path, progress_callback)
    else:
        logger.warning(f"Unsupported file type: {file_type}")
        return False, "Unsupported file type."
