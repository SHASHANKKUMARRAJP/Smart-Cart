import sys
import warnings
warnings.filterwarnings("ignore")
from app.dress_scraper import extract_manual_metadata_from_url, generate_search_keywords

url = "https://amzn.in/d/0Jhwblz5"
res = extract_manual_metadata_from_url(url)
print(f"\\n--- METADATA ---")
for k, v in res.items():
    print(f"{k}: {v}")
    
print(f"\\n--- GENERATED QUERY ---")
print(generate_search_keywords(res))
