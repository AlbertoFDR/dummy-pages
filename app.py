import os
import time
import subprocess
from pathlib import Path
from flask import Flask, make_response, send_file, render_template_string


app = Flask(__name__)
DEBUG = True

# ======================== Process list
process_path_list = []

# -----------------------------> MANUAL HEADERS

# ======================== Content-Security-Policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy
# Content-Security-Policy: <policy-directive>; <policy-directive>
# === Directives:
# default-src, script-src, script-src-elem, script-src-attr, style-src, style-src-elem, style-src-attr, img-src, connect-src, font-src, object-src, media-src, frame-src, sandbox, report-uri, child-src, form-action, frame-ancestors, base-uri, report-to, worker-src, manifest-src, prefetch-src, navigate-to, upgrade-insecure-requests, 
# === Reporting directives
# Security-Policy-Report-only, report-uri, report-to
# === Experimental
# require-trusted-types-for, trusted-types 
# === Deprecated
# block-all-mixed-content, plugin-types, referrer 
csp_value = -1
# Examples from:
# https://content-security-policy.com/examples/
csp_list = [
    "default-src 'self'; img-src 'self' cdn.example.com;",
    "script-src js-cdn.example.com 'nonce-rAnd0m';",
    "style-src css-cdn.example.com 'nonce-rAnd0m';",
    "",
]


# ======================== Permissions-Policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy
# Permissions-Policy: <directive> <allowlist>
# === Directives:
# 'accelerometer', 'ambient-light-sensor', 'autoplay', 'battery', 'camera', 'display-capture', 'document-domain', 'encrypted-media', 'execution-while-not-rendered', 'execution-while-out-of-viewport', 'fullscreen', 'gamepad', 'geolocation', 'gyroscope', 'hid', 'identity-credentials-get', 'idle-detection', 'local-fonts', 'magnetometer', 'microphone', 'midi', 'otp-credentials', 'payment', 'picture-in-picture', 'publickey-credentials-create', 'publickey-credentials-get', 'screen-wake-lock', 'serial', 'speaker-selection', 'storage-access', 'usb', 'web-share', 'window-management', 'xr-spatial-tracking'
pp_value = -1 
pp_list = [
    "geolocation=*",
    "geolocation=(self 'https://a.example.com' 'https://b.example.com')",
    "picture-in-picture=(), geolocation=(self https://example.com), camera=*",
]


# From StackOverflow:
# https://stackoverflow.com/questions/37427683/python-search-for-a-file-in-current-directory-and-all-its-parents/70859914#70859914
def find_upwards(cwd: Path, filename: str) -> Path | None:
    if cwd == Path(cwd.root) or cwd == cwd.parent:
        return None
    fullpath = cwd / filename
    return fullpath if fullpath.exists() else find_upwards(cwd.parent, filename)


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>')
def dir(req_path):
    BASE_DIR = './'
    abs_path = os.path.join(BASE_DIR, req_path)

    # Exist?
    if not os.path.exists(abs_path):
        return ""

    # ============ HTML file
    if os.path.isfile(abs_path):
        response = make_response(send_file(abs_path))

        # ====================================== file run.sh 
        # For the case of <iframe>, creates another process to simulate another origin
        run_sh = str(find_upwards(Path(abs_path), "run.sh"))
        if run_sh != 'None' and run_sh not in process_path_list:
            popen = subprocess.Popen(run_sh)
            time.sleep(1)
            returncode = popen.poll()
            if returncode is None:
                process_path_list.append(run_sh)
            else:
                # Avoid address in use?
                if returncode != 98:
                    print("??????????????????????????????????????????????????")
                    print("[ERROR] Why the helll *****")
                    print(f"WE COULD NOT CREATE PROCESS OF {run_sh}. CHECK PLEASE {returncode}")
                    print("??????????????????????????????????????????????????")

        if DEBUG:
            print(f"""
            ----------------
                  Endpoint: {abs_path}
                  run.sh: {run_sh}
                  run.sh list: {process_path_list}
            ----------------
            """)

        # ====================================== HEADERS
        # === CSP HEADER
        # Check if the file has a CSP associated
        csp_file = abs_path[:-5] + ".csp"  # delete .html
        csp = ""
        if os.path.exists(csp_file):
            response.headers['Content-Security-Policy'] = open(csp_file, 'r').read().replace('\n', '')
            csp = open(csp_file, 'r').read().replace('\n', '')
        elif csp_value > -1:
            response.headers['Content-Security-Policy'] = csp_list[csp_value]
            csp = csp_list[csp_value]
        
        # === PERMISSION POLICY HEADER
        # Check if the file has a PP file associated
        pp_file = abs_path[:-5] + ".pp"  # delete .html
        pp = ""
        if os.path.exists(pp_file):
            response.headers['Permissions-Policy'] = open(pp_file, 'r').read().replace('\n', '') 
            pp = open(pp_file, 'r').read().replace('\n', '') 
        elif pp_value > -1:
            response.headers['Permissions-Policy'] = pp_list[pp_value] 
            pp = pp_list[value]
        # =======================================
        print(f"""
        # =============== {abs_path} ===============
        Security Headers:
              CSP: {csp}
              Permission-Policy: {pp}
        # ======================================================================
        """)
        return response

    # =========== List dirs
    files = os.listdir(abs_path)
    template = """
<ul>
    {% for file in files %}
    <li>
        <a href="{{ (request.path + '/' if request.path != '/' else '') + file }}">
            {{ (request.path + '/' if request.path != '/' else '') + file }}
        </a>
    </li>
    {% endfor %}
</ul>
    """
    return render_template_string(template, files=files)


if __name__ == "__main__":
    # run
    app.run(debug=True)
