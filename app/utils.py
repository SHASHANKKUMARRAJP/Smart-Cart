from flask import jsonify

def generate_deep_links(platform, product, product_url):
    """Generate deep links for mobile apps"""
    
    # Platform-specific deep link schemes
    if product_url and product_url != f"https://blinkit.com/search?q={product.replace(' ', '%20')}" and product_url != f"https://www.zeptonow.com/search?q={product.replace(' ', '%20')}" and product_url != f"https://www.swiggy.com/instamart/search?q={product.replace(' ', '%20')}":
        # Use actual product URL for deep linking
        if platform == "Blinkit":
            # Extract product ID from URL for better deep linking
            product_path = product_url.replace('https://blinkit.com', '')
            deep_links = {
                "android": f"intent://blinkit.com{product_path}#Intent;scheme=https;package=com.blinkit;S.browser_fallback_url={product_url};end",
                "ios": f"blinkit{product_path}",
                "web": product_url
            }
        elif platform == "Zepto":
            product_path = product_url.replace('https://www.zeptonow.com', '')
            deep_links = {
                "android": f"zepto://app{product_path}",
                "ios": f"zepto://app{product_path}",
                "web": product_url
            }
        elif platform == "Instamart":
            product_path = product_url.replace('https://www.swiggy.com/instamart', '')
            deep_links = {
                "android": f"intent://www.swiggy.com/instamart{product_path}#Intent;scheme=https;package=com.swiggy.android;S.browser_fallback_url={product_url};end",
                "ios": f"swiggy://instamart{product_path}",
                "web": product_url
            }
        else:
             deep_links = {}
    else:
        # Fallback to search deep links with proper app schemes
        deep_links = {
            "Blinkit": {
                "android": "intent://blinkit.com/search#Intent;scheme=https;package=com.blinkit;S.browser_fallback_url=https://blinkit.com/search?q=" + product.replace(' ', '%20') + ";end",
                "ios": "blinkit://search?q=" + product.replace(' ', '%20'),
                "web": f"https://blinkit.com/search?q={product.replace(' ', '%20')}"
            },
            "Zepto": {
                "android": "zepto://app/search?q=" + product.replace(' ', '%20'),
                "ios": "zepto://app/search?q=" + product.replace(' ', '%20'),
                "web": f"https://www.zeptonow.com/search?q={product.replace(' ', '%20')}"
            },
            "Instamart": {
                "android": "intent://www.swiggy.com/instamart/search#Intent;scheme=https;package=com.swiggy.android;S.browser_fallback_url=https://www.swiggy.com/instamart/search?q=" + product.replace(' ', '%20') + ";end",
                "ios": "swiggy://instamart/search?q=" + product.replace(' ', '%20'),
                "web": f"https://www.swiggy.com/instamart/search?q={product.replace(' ', '%20')}"
            }
        }.get(platform, {})
    
    return deep_links

def get_app_store_links(platform):
    app_store_links = {
        "Blinkit": {
            "android": "https://play.google.com/store/apps/details?id=com.blinkit",
            "ios": "https://apps.apple.com/app/blinkit-grocery-delivery/id14792899056"
        },
        "Zepto": {
            "android": "https://play.google.com/store/apps/details?id=com.zeptoconsumerapp",
            "ios": "https://apps.apple.com/app/zepto-instant-grocery/id1472456744"
        },
        "Instamart": {
            "android": "https://play.google.com/store/apps/details?id=com.swiggy.android",
            "ios": "https://apps.apple.com/app/swiggy-food-grocery-delivery/id981434769"
        }
    }
    return app_store_links.get(platform, {})
