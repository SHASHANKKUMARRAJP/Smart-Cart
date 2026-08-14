import sys
import warnings
warnings.filterwarnings("ignore")
from app.dress_scraper import extract_manual_metadata_from_url

urllist = [
    "https://www.zara.com/in/en/floral-print-midi-dress-p01234567.html",
    "https://www.urbanic.com/product/floral-dress-12345",
    "https://shop.mango.com/in/women/dresses-and-jumpsuits/bow-neck-cut-out-detail-dress_67025983.html"
]

for u in urllist:
    res = extract_manual_metadata_from_url(u)
    print(f"URL: {u}\\nBRAND: {res.get('brand')}\\n")
