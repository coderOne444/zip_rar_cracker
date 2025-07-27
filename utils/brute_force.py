import zipfile
import itertools
from multiprocessing import Process, Event, Manager, cpu_count


def try_password(zip_path, password):
    try:
        with zipfile.ZipFile(zip_path) as zf:
            zf.extractall(pwd=password.encode())
        print(f"✅ Password found: {password}")
        return True
    except (RuntimeError, zipfile.BadZipFile, zipfile.LargeZipFile):
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def brute_force_worker(zip_path, combos, stop_event, found_password, progress_counter, progress_callback=None):
    for combo in combos:
        if stop_event.is_set():
            return
        password = ''.join(combo)
        if try_password(zip_path, password):
            found_password.append(password)
            stop_event.set()
            return
        with progress_counter.get_lock():
            progress_counter.value += 1
            if progress_callback and progress_counter.value % 100 == 0:
                progress_callback(progress_counter.value)

def threaded_brute_force(zip_path, charset, max_len, num_threads=None, on_result=None, progress_callback=None):
    if num_threads is None:
        num_threads = cpu_count()
    manager = Manager()
    stop_event = manager.Event()
    found_password = manager.list()
    from multiprocessing import Value
    progress_counter = Value('i', 0)
    total = sum(len(charset) ** l for l in range(1, max_len + 1))
    for length in range(1, max_len + 1):
        combos = list(itertools.product(charset, repeat=length))
        chunk_size = (len(combos) + num_threads - 1) // num_threads
        processes = []
        for i in range(num_threads):
            chunk = combos[i*chunk_size:(i+1)*chunk_size]
            if not chunk:
                continue
            p = Process(target=brute_force_worker, args=(zip_path, chunk, stop_event, found_password, progress_counter, progress_callback))
            p.start()
            processes.append(p)
        for p in processes:
            p.join()
        if stop_event.is_set():
            break
    if stop_event.is_set() and found_password:
        print(f"✅ Password found: {found_password[0]}")
        if on_result:
            on_result(True, found_password[0])
        return found_password[0]
    else:
        print("❌ Password not found.")
        if on_result:
            on_result(False, None)
        return None

if __name__ == "__main__":
    # Example usage
    zip_path = "protected.zip"
    charset = "abc123"
    max_len = 4
    threaded_brute_force(zip_path, charset, max_len)
