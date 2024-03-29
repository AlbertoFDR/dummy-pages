# dummy-pages

I create this project as testing environment. In other words, this toy project allows emulating more than one origin (creating two listen ports 1234 and 5000) and to check how the browser works with a different set of server headers (e.g., CSP, Permissions-policies, ...). It should work the secure origin for testing (localhost/127.0.0.1) because is usually (NOT ALWAYS) considered as [trustworthy origin](https://www.w3.org/TR/secure-contexts/#is-origin-trustworthy).

## Install

```bash
# Edit /etc/hosts
# Add the following entry
127.0.0.1 dummy.local dummy2.local 

# Use the script to install the cert in the Browser as trusted CA 
./install_cert
```

## Other similar projects
- https://github.com/GoogleChrome/samples/tree/gh-pages -- https://googlechrome.github.io/samples/allow-popups-to-escape-sandbox/index.html
- https://public-firing-range.appspot.com/urldom/index.html
- https://canhas.report/permissions-policy
- https://dev-pages.brave.software/
- https://webdbg.com/test/
- Chromium web tests itself: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/ 
- Web-platform-tests Project: https://wpt.live/
