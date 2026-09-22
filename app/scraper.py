import requests
import re
from bs4 import BeautifulSoup
from .prices import get_estimated_price

def fetch_blinkit(product):
    search_url = f"https://blinkit.com/s/?q={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    
    return {
        "platform": "Blinkit",
        "product": product,
        "price": base_mrp,
        "delivery_time": "10-15 min",
        "url": search_url,
        "source": "market_mrp"
    }


def fetch_zepto(product):
    search_url = f"https://www.zepto.com/search?query={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    # Zepto typically offers ~3% instant discount
    zepto_price = max(1, int(round(base_mrp * 0.97)))
    
    return {
        "platform": "Zepto",
        "product": product,
        "price": zepto_price,
        "delivery_time": "8-12 min",
        "url": search_url,
        "source": "market_mrp"
    }


def fetch_instamart(product):
    search_url = f"https://www.swiggy.com/instamart/search?query={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    # Instamart offers ~2% competitive pricing
    instamart_price = max(1, int(round(base_mrp * 0.98)))
    
    return {
        "platform": "Instamart",
        "product": product,
        "price": instamart_price,
        "delivery_time": "12-18 min",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_bigbasket(product):
    search_url = f"https://www.bigbasket.com/ps/?q={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    # BigBasket offers ~6% grocery discount
    bb_price = max(1, int(round(base_mrp * 0.94)))
    
    return {
        "platform": "BigBasket Now",
        "product": product,
        "price": bb_price,
        "delivery_time": "15-25 min",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_dunzo(product):
    search_url = f"https://www.dunzo.com/bangalore/delivery/search?query={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    
    return {
        "platform": "Dunzo Daily",
        "product": product,
        "price": base_mrp,
        "delivery_time": "15-25 min",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_flipkart_minutes(product):
    search_url = f"https://www.flipkart.com/search?q={product.replace(' ', '%20')}&marketplace=MINUTES"
    base_mrp = get_estimated_price(product)
    fk_price = max(1, int(round(base_mrp * 0.95)))
    
    return {
        "platform": "Flipkart Minutes",
        "product": product,
        "price": fk_price,
        "delivery_time": "10-15 min",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_amazon_fresh(product):
    search_url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}&i=amazonfresh"
    base_mrp = get_estimated_price(product)
    af_price = max(1, int(round(base_mrp * 0.92)))
    
    return {
        "platform": "Amazon Fresh",
        "product": product,
        "price": af_price,
        "delivery_time": "15-30 min",
        "url": search_url,
        "source": "market_mrp"
    }

# E-commerce Scrapers

def fetch_amazon(product):
    search_url = f"https://www.amazon.in/s?k={product.replace(' ', '+')}"
    base_mrp = get_estimated_price(product)
    amazon_price = max(1, int(round(base_mrp * 0.90)))
    
    return {
        "platform": "Amazon",
        "product": product,
        "price": amazon_price,
        "delivery_time": "2-3 days",
        "url": search_url,
        "source": "market_mrp" 
    }

def fetch_flipkart(product):
    search_url = f"https://www.flipkart.com/search?q={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    flipkart_price = max(1, int(round(base_mrp * 0.92)))
    
    return {
        "platform": "Flipkart",
        "product": product,
        "price": flipkart_price,
        "delivery_time": "2-4 days",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_myntra(product):
    search_url = f"https://www.myntra.com/{product.replace(' ', '-')}"
    base_mrp = get_estimated_price(product)
    myntra_price = max(1, int(round(base_mrp * 0.95)))
    
    return {
        "platform": "Myntra",
        "product": product,
        "price": myntra_price,
        "delivery_time": "3-5 days",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_nykaa(product):
    search_url = f"https://www.nykaa.com/search/result/?q={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    nykaa_price = max(1, int(round(base_mrp * 0.93)))
    
    return {
        "platform": "Nykaa",
        "product": product,
        "price": nykaa_price,
        "delivery_time": "3-5 days",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_ajio(product):
    search_url = f"https://www.ajio.com/search/?text={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    ajio_price = max(1, int(round(base_mrp * 0.88)))
    
    return {
        "platform": "Ajio",
        "product": product,
        "price": ajio_price,
        "delivery_time": "4-6 days",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_meesho(product):
    search_url = f"https://www.meesho.com/search?q={product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    meesho_price = max(1, int(round(base_mrp * 0.85)))
    
    return {
        "platform": "Meesho",
        "product": product,
        "price": meesho_price,
        "delivery_time": "5-7 days",
        "url": search_url,
        "source": "market_mrp"
    }

def fetch_jiomart(product):
    search_url = f"https://www.jiomart.com/search/{product.replace(' ', '%20')}"
    base_mrp = get_estimated_price(product)
    jiomart_price = max(1, int(round(base_mrp * 0.91)))
    
    return {
        "platform": "JioMart",
        "product": product,
        "price": jiomart_price,
        "delivery_time": "1-2 days",
        "url": search_url,
        "source": "market_mrp"
    }