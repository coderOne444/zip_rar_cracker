# web_app/app.py
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import time
from zip_rar_cracker import crack_file

UPLOAD_FOLDER = "web_app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    if request.method == "POST":
        if 'protected_file' not in request.files or 'wordlist_file' not in request.files:
            error = "Missing files."
        else:
            file_type = request.form.get("file_type", "ZIP").upper()
            enc_file = request.files['protected_file']
            wordlist = request.files['wordlist_file']

            enc_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(enc_file.filename))
            wordlist_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(wordlist.filename))
            enc_file.save(enc_path)
            wordlist.save(wordlist_path)

            def progress_callback(count):
                pass  # Optional: Implement live progress with WebSockets or polling

            start = time.time()
            success, pwd = crack_file(enc_path, wordlist_path, file_type, progress_callback)
            end = time.time()

            if success:
                result = f"✅ Password Found: {pwd} (Time: {int(end-start)}s)"
            else:
                error = f"❌ {pwd} (Took {int(end-start)}s)"

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
