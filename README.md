# dummy-pages

I create this project as testing environment. In other words, this toy project allows emulating more than one origin (`dummyX.local`&`app.dummyX.local`) and to check how the browser works with a different set of server headers and configurations (e.g., CSP, Cookies, Permissions-policies, ...). 

## Install

```bash
# Edit /etc/hosts
sudo echo "# dummy-pages" >> /etc/hosts
sudo echo "127.0.0.1 dummy.local dummy2.local dummy3.local" >> /etc/hosts 
sudo echo "127.0.0.1 app.dummy.local app.dummy2.local app.dummy3.local >> /etc/hosts
```

## Run

```bash
# Needs the sudo for opening port 443
# No malware I promise
sudo python3 app.py

# Visit https://dummy.local/ on the browser
```

## Other test pages
- https://github.com/GoogleChrome/samples/tree/gh-pages -- https://googlechrome.github.io/samples/allow-popups-to-escape-sandbox/index.html
- https://public-firing-range.appspot.com/urldom/index.html
- https://canhas.report/permissions-policy
- https://dev-pages.brave.software/
- https://webdbg.com/test/
- Chromium web tests itself: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/ 
- Web-platform-tests Project: https://wpt.live/
