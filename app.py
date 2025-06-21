from flask import Flask, request, render_template, render_template_string, redirect, url_for, flash, send_from_directory
import subprocess
import requests
import os
from werkzeug.utils import secure_filename
import urllib3

# Disable insecure request warnings from requests (for Kubernetes API calls with verify=False)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.secret_key = 'kubepwn_secret_key'

UPLOAD_FOLDER = '/var/www/html/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/instructions")
def instructions():
    return render_template("instructions/instructions.html")



# --- Remote Code Execution (RCE) ---
@app.route('/rce', methods=['GET'])
def rce():
    cmd = request.args.get('cmd')
    result = None
    if cmd:
        try:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate(timeout=5)
            result = stdout.decode() + stderr.decode()
        except subprocess.TimeoutExpired:
            result = "Command timed out"
        except Exception as e:
            result = f"Error: {e}"
    return render_template('rce.html', result=result)



# --- Server Side Template Injection (SSTI) ---
@app.route('/ssti', methods=['GET', 'POST'])
def ssti():
    if request.method == 'POST':
        template = request.form.get('template')
    else:
        template = request.args.get('template')

    if template:
        try:
            return render_template_string(template)
        except Exception as e:
            return f"Template error: {e}", 400

    return render_template('ssti.html')


# --- Server Side Request Forgery (SSRF) ---
@app.route('/ssrf', methods=['GET'])
def ssrf():
    url = request.args.get('url')
    response = None
    if url:
        try:
            res = requests.get(url, timeout=5)
            response = f"Status: {res.status_code}\n\nContent:\n{res.text[:1000]}"
        except Exception as e:
            response = f"Error: {e}"
    return render_template('ssrf.html', response=response)



# --- File Upload ---
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        filename = secure_filename(f.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(filepath)
        flash(f'File uploaded to {filepath}')
        return redirect(url_for('upload'))
    return render_template('upload.html')


# --- Serve uploaded files ---
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# --- Privilege Escalation demo ---
@app.route('/priv-esc')
def priv_esc():
    checks = []
    checks.append("Checking Docker socket: " + ("FOUND" if os.path.exists("/var/run/docker.sock") else "NOT FOUND"))
    try:
        out = subprocess.getoutput("docker ps")
        checks.append("Docker access check:\n" + out)
    except Exception as e:
        checks.append(f"Docker error: {e}")
    return "<pre>" + "\n\n".join(checks) + "</pre>"




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
