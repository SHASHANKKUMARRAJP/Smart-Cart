import requests
import random
import re
from bs4 import BeautifulSoup
from .prices import get_estimated_price

def fetch_blinkit(product):
    # Enhanced headers to bypass CloudFront protection (kept for potential future use)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    
    search_url = f"https://blinkit.com/s/?q={product.replace(' ', '%20')}"
    
    # Return estimated data with Search URL for reliability
    estimated_price = get_estimated_price(product)
    blinkit_price = estimated_price + random.randint(0, 15)
    
    return {
        "platform": "Blinkit",
        "product": product,
        "price": blinkit_price,
        "delivery_time": f"{random.randint(8, 15)} min",
        "url": search_url,
        "source": "estimated"
    }


def fetch_zepto(product):
    search_url = f"https://www.zepto.com/search?query={product.replace(' ', '%20')}"
    
    # Return estimated data with Search URL for reliability
    estimated_price = get_estimated_price(product)
    zepto_price = estimated_price + random.randint(-8, 5)
    
    return {
        "platform": "Zepto",
        "product": product,
        "price": zepto_price,
        "delivery_time": f"{random.randint(6, 14)} min",
        "url": search_url,
        "source": "estimated"
    }


def fetch_instamart(product):
    search_url = f"https://www.swiggy.com/instamart/search?query={product.replace(' ', '%20')}"
    
    # Return estimated data with Search URL for reliability
    estimated_price = get_estimated_price(product)
    instamart_price = estimated_price + random.randint(-5, 12)
    
    return {
        "platform": "Instamart",
        "product": product,
        "price": instamart_price,
        "delivery_time": f"{random.randint(10, 20)} min",
        "url": search_url,
        "source": "estimated"
    }

def fetch_bigbasket(product):
    search_url = f"https://www.bigbasket.com/ps/?q={product.replace(' ', '%20')}"
    estimated_price = get_estimated_price(product)
    bb_price = estimated_price + random.randint(-10, 8)
    return {
        "platform": "BigBasket Now",
        "product": product,
        "price": bb_price,
        "delivery_time": f"{random.randint(10, 20)} min",
        "url": search_url,
        "source": "estimated"
    }

def fetch_dunzo(product):
    search_url = f"https://www.dunzo.com/bangalore/delivery/search?query={product.replace(' ', '%20')}"
    estimated_price = get_estimated_price(product)
    dunzo_price = estimated_price + random.randint(-5, 15)
    return {
        "platform": "Dunzo Daily",
        "product": product,
        "price": dunzo_price,
        "delivery_time": f"{random.randint(12, 25)} min",
        "url": search_url,
        "source": "estimated"
    }

def fetch_flipkart_minutes(product):
    search_url = f"https://www.flipkart.com/search?q={product.replace(' ', '%20')}&marketplace=MINUTES"
    estimated_price = get_estimated_price(product)
    fk_price = estimated_price + random.randint(-3, 10)
    return {
        "platform": "Flipkart Minutes",
        "product": product,
        "price": fk_price,
        "delivery_time": f"{random.randint(8, 15)} min",
        "url": search_url,
        "source": "estimated"
    }

def fetch_amazon_fresh(product):
    search_url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}&i=amazonfresh"
    estimated_price = get_estimated_price(product)
    af_price = estimated_price + random.randint(-8, 5)
    return {
        "platform": "Amazon Fresh",
        "product": product,
        "price": af_price,
        "delivery_time": f"{random.randint(10, 20)} min",
        "url": search_url,
        "source": "estimated"
    }

# E-commerce Scrapers

def fetch_amazon(product):
    try:
        # Heavily protected, likely to fall back, but we attempt
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }
        search_url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}"
        
        # Real scraping often fails on Amazon without proxies/selenium
        # We simulate a reasonable ecommerce price variation
        estimated_price = get_estimated_price(product)
        # Ecommerce usually cheaper than quick commerce
        amazon_price = int(estimated_price * 0.9) 
        
        return {
            "platform": "Amazon",
            "product": product,
            "price": amazon_price,
            "delivery_time": "2-3 days",
            "url": search_url,
            "source": "simulated" 
        }
    except Exception:
        estimated_price = get_estimated_price(product)
        return {
            "platform": "Amazon",
            "product": product,
            "price": int(estimated_price * 0.9),
            "delivery_time": "2-3 days",
            "url": f"https://www.amazon.in/s?k={product.replace(' ', '+')}",
            "source": "estimated"
        }

def fetch_flipkart(product):
    try:
        headers = {
             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        search_url = f"https://www.flipkart.com/search?q={product.replace(' ', '%20')}"
        
        estimated_price = get_estimated_price(product)
        flipkart_price = int(estimated_price * 0.92)
        
        return {
            "platform": "Flipkart",
            "product": product,
            "price": flipkart_price,
            "delivery_time": "2-4 days",
            "url": search_url,
            "source": "simulated"
        }
    except Exception:
         return {
            "platform": "Flipkart",
            "product": product,
            "price": 0,
            "delivery_time": "Unavailable",
            "url": "",
            "source": "error"
        }

def fetch_myntra(product):
    search_url = f"https://www.myntra.com/{product.replace(' ', '-')}"
    estimated_price = get_estimated_price(product)
    myntra_price = int(estimated_price * 0.95)
    return {
        "platform": "Myntra",
        "product": product,
        "price": myntra_price,
        "delivery_time": "3-5 days",
        "url": search_url,
        "source": "simulated"
    }

def fetch_nykaa(product):
    search_url = f"https://www.nykaa.com/search/result/?q={product.replace(' ', '%20')}"
    estimated_price = get_estimated_price(product)
    nykaa_price = int(estimated_price * 0.93)
    return {
        "platform": "Nykaa",
        "product": product,
        "price": nykaa_price,
        "delivery_time": "3-5 days",
        "url": search_url,
        "source": "simulated"
    }

def fetch_ajio(product):
    search_url = f"https://www.ajio.com/search/?text={product.replace(' ', '%20')}"
    estimated_price = get_estimated_price(product)
    ajio_price = int(estimated_price * 0.88)
    return {
        "platform": "Ajio",
        "product": product,
        "price": ajio_price,
        "delivery_time": "4-6 days",
        "url": search_url,
        "source": "simulated"
    }

def fetch_meesho(product):
    search_url = f"https://www.meesho.com/search?q={product.replace(' ', '%20')}"
    estimated_price = get_estimated_price(product)
    meesho_price = int(estimated_price * 0.85) # Usually cheaper
    return {
        "platform": "Meesho",
        "product": product,
        "price": meesho_price,
        "delivery_time": "5-7 days",
        "url": search_url,
        "source": "simulated"
    }