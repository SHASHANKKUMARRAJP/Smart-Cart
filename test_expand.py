import requests

url = "https://amzn.in/d/0Jhwblz5"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
}

print("--- Requests GET ---")
try:
    resp = requests.get(url, headers=headers, allow_redirects=True, timeout=5)
    print("Status:", resp.status_code)
    print("Final URL:", resp.url)
except Exception as e:
    print("GET failed:", e)
