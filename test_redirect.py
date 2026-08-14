import urllib.request
from urllib.error import URLError, HTTPError
url = "https://amzn.in/d/0Jhwblz5"

class HeadRequest(urllib.request.Request):
    def get_method(self):
        return "HEAD"

try:
    req = urllib.request.Request(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        }
    )
    res = urllib.request.urlopen(req, timeout=5)
    print("Resolved URL:", res.url)
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.reason)
    print("Error headers:", e.headers)
except Exception as e:
    print("Error:", e)
