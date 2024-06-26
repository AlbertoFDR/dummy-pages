import os
from urllib.parse import urlparse
from flask import Flask, request, make_response, send_file, render_template_string


app = Flask(__name__)
DEBUG = True
BASE_DIR = './testing-pages/'
ORIGIN_NEED_HEADER = ["dummy.local"]
ENDPOINT_NEED_HEADER = ["./testing-pages/iframes/about.html"]

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
    "default-src 'none'; script-src https://dummy.local/; child-src 'self' *;",
    "default-src 'self'; img-src 'self' cdn.example.com;",
    #"script-src js-cdn.example.com 'nonce-rAnd0m' 'unsafe-inline';",
    "script-src 'unsafe-inline';",
    "style-src css-cdn.example.com 'nonce-rAnd0m';",
    "default-src 'self'; script-src 'unsafe-inline'; frame-src dummy.local",
    "",
]


# ======================== Permissions-Policy
# https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Permissions-Policy
# Permissions-Policy: <directive> <allowlist>
# === Directives:
# 'accelerometer', 'ambient-light-sensor', 'autoplay', 'battery', 'camera', 'display-capture', 'document-domain', 'encrypted-media', 'execution-while-not-rendered', 'execution-while-out-of-viewport', 'fullscreen', 'gamepad', 'geolocation', 'gyroscope', 'hid', 'identity-credentials-get', 'idle-detection', 'local-fonts', 'magnetometer', 'microphone', 'midi', 'otp-credentials', 'payment', 'picture-in-picture', 'publickey-credentials-create', 'publickey-credentials-get', 'screen-wake-lock', 'serial', 'speaker-selection', 'storage-access', 'usb', 'web-share', 'window-management', 'xr-spatial-tracking'
pp_value = -1
pp_list = [
    "geolocation=()",
    "geolocation=*",
    "geolocation=('https://dummy.local')",
    "picture-in-picture=(), geolocation=(self https://example.com), camera=*",
]


@app.route('/', defaults={'req_path': ''})
@app.route('/<path:req_path>', methods=['GET', 'POST'])
def dir(req_path):
    global BASE_DIR
    abs_path = os.path.join(BASE_DIR, req_path)

    # Exist?
    if not os.path.exists(abs_path):
        return ""

    # ============ HTML file
    if os.path.isfile(abs_path):
        response = make_response(send_file(abs_path))

        if DEBUG:
            print(f"""
            ----------------
                  Domain: {request.url_root}
                  Endpoint: {abs_path}
                  Cookie: {request.cookies}
            ----------------
            """)

        # Need header
        csp = ""
        pp = ""
        report_to = ""
        pp_report = ""
        #  Blacklist for header some file "example.html" not in abs_path
        if urlparse(request.url_root).netloc in ORIGIN_NEED_HEADER or abs_path in ENDPOINT_NEED_HEADER:
            # ====================================== HEADERS
            # === CSP HEADER
            # Check if the file has a CSP associated
            csp_file = abs_path[:-5] + ".csp"  # delete .html
            if os.path.exists(csp_file):
                response.headers['Content-Security-Policy'] = open(csp_file, 'r').read().replace('\n', '')
                csp = open(csp_file, 'r').read().replace('\n', '')
            elif csp_value > -1:
                response.headers['Content-Security-Policy'] = csp_list[csp_value]
                csp = csp_list[csp_value]
            
            # === PERMISSION POLICY HEADER
            # Check if the file has a PP file associated
            pp_file = abs_path[:-5] + ".pp"  # delete .html
            if os.path.exists(pp_file):
                response.headers['Permissions-Policy'] = open(pp_file, 'r').read().replace('\n', '') 
                pp = open(pp_file, 'r').read().replace('\n', '') 
            elif pp_value > -1:
                response.headers['Permissions-Policy'] = pp_list[pp_value] 
                pp = pp_list[pp_value]
            
            # === Reporting
            report_to = '{"group":"default","max_age":1800,"endpoints":[{"url":"https://prueba.report-uri.com/a/d/g"}],"include_subdomains":true}'
            pp_report = "fullscreen=()"
            # response.headers['Permissions-Policy'] = "fullscreen=*"
            # response.headers['Report-To'] = report_to
            # response.headers['Permissions-Policy-Report-Only'] = pp_report 
            #response.headers['Reporting-Endpoints'] = 'main-endpoint="https://webhook.site/7c05a5c7-9e36-478a-842b-cdcee58bc52a/main", default="https://webhook.site/7c05a5c7-9e36-478a-842b-cdcee58bc52a/default"'

            # Add more headers
            # POST+Lax test
            #response.headers['Set-Cookie'] = "user=John; secure; HttpOnly; path=/; expires=Tue, 19 Jan 2038 03:14:07 GMT;"
        # =======================================
        print(f"""
        # =============== {abs_path} ===============
        Security Headers:
              CSP: {csp}
              Permission-Policy: {pp}
              Report-to: {report_to}
              Permissions-Policy-Report-Only: {pp_report}
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
    app.run(
        host="127.0.0.1",
        port="443",
        ssl_context=('cert/localhost.crt', 'cert/localhost.key'),
        debug=True)
