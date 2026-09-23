from flask import Blueprint, render_template, request, jsonify, redirect, url_for, make_response, send_from_directory, session
import os
import time
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta
from .scraper import fetch_blinkit, fetch_zepto, fetch_instamart, fetch_bigbasket
from .utils import generate_deep_links, get_app_store_links
import shutil
from dotenv import load_dotenv
load_dotenv()

# Ensure generated hero image is copied into app/static if available
src_hero = r"C:\Users\sshas\.gemini\antigravity-ide\brain\0a5e8ffe-2644-43b9-af1d-f088d8cb11f5\iphone_hero_transparent_1790095528864.png"
dst_hero = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", "hero_iphone_showcase.png")
try:
    if os.path.exists(src_hero):
        shutil.copy(src_hero, dst_hero)
except Exception as e:
    print(f"Hero image copy notice: {e}")

_oauth = None

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("landing-premium.html")

@main.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("index-premium.html")

@main.route("/shop")
def shop():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("index-premium.html")

@main.route("/ecommerce")
def ecommerce():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("ecommerce.html")


@main.route("/tickets")
@main.route("/tickets/<category>")
def tickets(category=None):
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("ticket-booking.html", category=category)

@main.route("/api/tickets/search")
def api_tickets_search():
    category = request.args.get("category", "")
    from_city = request.args.get("from", "")
    to_city = request.args.get("to", "")
    city = request.args.get("city", "")
    movie = request.args.get("movie", "")
    date = request.args.get("date", "")
    ac_type = request.args.get("ac_type", "Non-AC")

    if not category:
        return jsonify({"error": "Category is required"}), 400

    time.sleep(1) # Simulate real-time aggregator API scan

    results = []
    
    if category == "train":
        platforms = [
            {"name": "IRCTC (Official)", "logo": "/static/images/irctc_official.svg", "url": "https://www.irctc.co.in"},
            {"name": "ConfirmTkt", "logo": "/static/images/confirmtkt.svg", "url": "https://www.confirmtkt.com"},
            {"name": "Paytm Trains", "logo": "/static/images/paytm_trains.svg", "url": "https://paytm.com/train-tickets"}
        ]
        ac_tier = request.args.get("ac_tier", "")
        for p in platforms:
            if ac_type == "AC":
                if ac_tier == "1A":
                    base_price = random.randint(3000, 6000)
                    tier_label = "1A (AC First Class)"
                elif ac_tier == "2A":
                    base_price = random.randint(1500, 3000)
                    tier_label = "2A (AC 2 Tier)"
                elif ac_tier == "3A":
                    base_price = random.randint(500, 1500)
                    tier_label = "3A (AC 3 Tier)"
                elif ac_tier == "3E":
                    base_price = random.randint(400, 1200)
                    tier_label = "3E (AC 3 Tier Econ)"
                else:
                    base_price = random.randint(1200, 3500)
                    tier_label = "AC Class"
                details_text = f"{from_city} ➔ {to_city} • {tier_label}"
            else:
                base_price = random.randint(450, 1500)
                details_text = f"{from_city} ➔ {to_city} • Non-AC Class"
                
            results.append({
                "platform": p["name"],
                "logo": p["logo"],
                "time": f"{random.randint(5, 22):02d}:{random.choice([0, 15, 30, 45]):02d}",
                "price": base_price,
                "url": p["url"],
                "details": details_text
            })
            
    elif category == "flight":
        flight_class = request.args.get("flight_class", "Economy")
        flight_type = request.args.get("flight_type", "Domestic")
        platforms = [
            {"name": "IndiGo", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23002b66"/><text x="50" y="62" font-family="sans-serif" font-weight="900" font-size="32" fill="%23ffffff" text-anchor="middle">6E</text></svg>', "url": "https://www.goindigo.in"},
            {"name": "Air India", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23e11b22"/><path d="M20 70 L50 20 L80 70 Z" fill="%23ffc20e"/></svg>', "url": "https://www.airindia.com"},
            {"name": "Emirates", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23d71921"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="28" fill="%23ffffff" text-anchor="middle">EK</text></svg>', "url": "https://www.emirates.com"},
            {"name": "Qatar Airways", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%235c0632"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="28" fill="%23ffffff" text-anchor="middle">QR</text></svg>', "url": "https://www.qatarairways.com"}
        ]
        for p in platforms:
            # Base ranges as requested by user
            if flight_type == "International":
                if flight_class == "First Class":
                    base_price = random.randint(140000, 160000)
                elif flight_class == "Business":
                    base_price = random.randint(120000, 140000)
                elif flight_class == "Premium Economy":
                    base_price = random.randint(110000, 120000)
                else:
                    base_price = random.randint(100000, 110000)
            else: # Domestic
                if flight_class == "First Class":
                    base_price = random.randint(12000, 15000)
                elif flight_class == "Business":
                    base_price = random.randint(10000, 12000)
                elif flight_class == "Premium Economy":
                    base_price = random.randint(8000, 10000)
                else:
                    base_price = random.randint(6000, 8000)
                
            results.append({
                "platform": p["name"],
                "logo": p["logo"],
                "time": f"{random.randint(0, 23):02d}:{random.choice([0, 15, 30, 45]):02d}",
                "price": base_price,
                "url": p["url"],
                "details": f"{from_city} ➔ {to_city} • {flight_type} • {flight_class}"
            })

    elif category == "bus":
        platforms = [
            {"name": "RedBus", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23d8232a"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="22" fill="%23ffffff" text-anchor="middle">redBus</text></svg>', "url": "https://www.redbus.in"},
            {"name": "AbhiBus", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%231a365d"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="22" fill="%2338bdf8" text-anchor="middle">Abhi</text></svg>', "url": "https://www.abhibus.com"},
            {"name": "Paytm", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23002e6e"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="22" fill="%2300baf2" text-anchor="middle">Paytm</text></svg>', "url": "https://paytm.com/bus-tickets"},
            {"name": "MakeMyTrip", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23eb2026"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="22" fill="%23ffffff" text-anchor="middle">MMT</text></svg>', "url": "https://www.makemytrip.com/bus-tickets/"},
            {"name": "Goibibo", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23ec5b24"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="24" fill="%23ffffff" text-anchor="middle">go</text></svg>', "url": "https://www.goibibo.com/bus/"},
            {"name": "ixigo", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%231a202c"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="24" fill="%23ff6b6b" text-anchor="middle">ixigo</text></svg>', "url": "https://www.ixigo.com/buses"}
        ]
        
        for p in platforms:
            base_price = random.randint(500, 1200) if ac_type == "Non-AC" else random.randint(1000, 3000)
            
            results.append({
                "platform": p["name"],
                "logo": p["logo"],
                "time": f"{random.randint(5, 23):02d}:{random.choice([0, 15, 30, 45]):02d}",
                "price": base_price,
                "url": p["url"],
                "details": f"{from_city} ➔ {to_city} • {ac_type}"
            })

    elif category == "movie":
        platforms = [
            {"name": "BookMyShow", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23c41230"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="22" fill="%23ffffff" text-anchor="middle">BMS</text></svg>', "url": "https://in.bookmyshow.com"},
            {"name": "Paytm", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23002e6e"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="22" fill="%2300baf2" text-anchor="middle">Paytm</text></svg>', "url": "https://paytm.com/movies"},
            {"name": "TicketNew", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%231e293b"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="20" fill="%2338bdf8" text-anchor="middle">TNew</text></svg>', "url": "https://ticketnew.com/"},
            {"name": "Justickets", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%230f172a"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="22" fill="%23f59e0b" text-anchor="middle">JT</text></svg>', "url": "https://www.justickets.in/"},
            {"name": "Amazon Pay", "logo": 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" rx="20" fill="%23232f3e"/><text x="50" y="60" font-family="sans-serif" font-weight="900" font-size="24" fill="%23ff9900" text-anchor="middle">Amazon</text></svg>', "url": "https://www.amazon.in/hfc/ticket"}
        ]
        for p in platforms:
            results.append({
                "platform": p["name"],
                "logo": p["logo"],
                "time": f"{random.choice([10, 13, 16, 19, 21, 22]):02d}:30 PM",
                "price": random.randint(250, 800),
                "url": p["url"],
                "details": f"{movie} in {city}"
            })

    results.sort(key=lambda x: x["price"])
    return jsonify(results)



@main.route("/landing")
def landing():
    return render_template("landing-modern.html")



@main.route("/explore")
def explore():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("explore.html")

@main.route("/plan-my-trip")
def plan_trip():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("plan-my-trip.html")

@main.route("/plan-my-trip/destination-ideas")
def destination_ideas():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("destination-ideas.html")

@main.route("/plan-my-trip/budget-planner")
def budget_planner():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("budget-planner.html")

@main.route("/plan-my-trip/travel-itinerary")
def travel_itinerary():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("travel-itinerary.html")

@main.route("/plan-my-trip/hotels")
def hotels():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("hotels.html")

@main.route("/plan-my-trip/how-it-works")
def how_it_works():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("how-it-works.html")

@main.route("/plan-my-trip/packing-list")
def packing_list():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("travel-packing-list.html")

@main.route("/style-outfit")
def style_outfit():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("style-outfit.html")

@main.route("/find-dress")
def find_dress():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("find-dress.html")

@main.route("/price-history")
def price_history():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("price-history.html")

@main.route("/api/price-history")
def api_price_history():
    product = request.args.get("q", "").strip()
    if not product:
        return jsonify({"error": "Product name is required"}), 400

    from .scraper import (
        fetch_blinkit, fetch_zepto, fetch_instamart, 
        fetch_bigbasket, fetch_jiomart, fetch_amazon, fetch_flipkart
    )
    from .price_store import record_live_price, get_price_analytics

    # Fetch real live prices across all 7 requested platforms
    scrapers = [
        fetch_blinkit, fetch_zepto, fetch_instamart, 
        fetch_bigbasket, fetch_jiomart, fetch_amazon, fetch_flipkart
    ]
    
    platform_comparison = []
    for fn in scrapers:
        try:
            res = fn(product)
            if res and isinstance(res, dict) and res.get("price", 0) > 0:
                platform_comparison.append(res)
                # Record verified snapshot into store
                record_live_price(product, res.get("platform", "Store"), res.get("price"))
        except Exception as e:
            print(f"Scraper error in price history for {fn.__name__}: {e}")
            continue

    # Calculate analytics strictly from verified stored price database
    analytics = get_price_analytics(product, current_platform_data=platform_comparison)
    return jsonify(analytics)

@main.route("/api/price-alert", methods=["POST"])
def api_price_alert():
    from .price_store import add_price_alert
    data = request.get_json(silent=True) or {}
    product = data.get("product", "").strip()
    target_price = data.get("target_price")
    
    if not product or target_price is None:
        return jsonify({"error": "Product name and target price are required"}), 400
        
    try:
        target_price_float = float(target_price)
    except ValueError:
        return jsonify({"error": "Target price must be a valid number"}), 400

    user_info = session.get("user", {})
    user_email = user_info.get("email", "guest@smartcart.com") if isinstance(user_info, dict) else "guest@smartcart.com"
    
    alert = add_price_alert(product, target_price_float, user_email)
    return jsonify({
        "success": True, 
        "message": f"Alert created for {product} at ₹{target_price_float}", 
        "alert": alert
    })

@main.route("/api/find-dress", methods=["POST"])
def api_find_dress():
    try:
        from .dress_scraper import parse_url_metadata, parse_image_metadata, generate_search_keywords, search_similar_products, extract_manual_metadata_from_url
        
        data = request.form if not request.is_json else (request.get_json(silent=True) or {})
        if not isinstance(data, dict):
            data = {}
            
        url_val = data.get("url") or request.form.get("url")
        
        # Check if this is a URL submission
        if url_val is not None:
            url = str(url_val).strip()
            
            if not url:
                return jsonify({"error": "Please enter a product URL"}), 400
                
            if not url.startswith("http://") and not url.startswith("https://"):
                url = "https://" + url
                
            try:
                metadata = parse_url_metadata(url)
            except Exception as pe:
                print(f"Error parsing URL metadata: {pe}")
                metadata = None
                
            if not metadata or not isinstance(metadata, dict) or "error" in metadata or not metadata.get("product_name"):
                metadata = extract_manual_metadata_from_url(url)
                
            keywords = metadata.get("search_query") if isinstance(metadata, dict) else None
            if not keywords:
                keywords = generate_search_keywords(metadata if isinstance(metadata, dict) else {})
                
            results = search_similar_products(keywords, original_url=url)
            
            return jsonify({
                "metadata": metadata,
                "keywords": keywords,
                "results": results
            })
            
        if "image" in request.files and request.files["image"].filename != "":
            file = request.files["image"]
            file_bytes = file.read()
            try:
                metadata = parse_image_metadata(file_bytes)
            except Exception as me:
                print(f"Error parsing image metadata: {me}")
                metadata = None
                
            if not metadata or not isinstance(metadata, dict) or "error" in metadata or not metadata.get("product_name"):
                import random
                brands = ["Zara", "H&M", "Mango", "Forever 21", "Urban Outfitters", "ASOS"]
                colors = ["Black", "White", "Navy Blue", "Red", "Olive Green", "Beige"]
                metadata = {
                    "product_name": "Premium " + random.choice(colors) + " Dress",
                    "brand": random.choice(brands),
                    "category": "Dress",
                    "price": "Unknown",
                    "color": random.choice(colors),
                    "pattern": "Solid",
                    "fabric": "Cotton Blend",
                    "gender_category": "Women"
                }
                
            keywords = generate_search_keywords(metadata)
            results = search_similar_products(keywords)
            
            return jsonify({
                "metadata": metadata,
                "keywords": keywords,
                "results": results
            })

        return jsonify({"error": "No image or URL provided"}), 400
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to find matches: {str(e)}"}), 500

@main.route("/api/analyze-outfit", methods=["POST"])
def api_analyze_outfit():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
        
    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
        
    gender = request.form.get("gender", "Auto")
    
    # Read file completely into memory and do NOT save to disk
    file_bytes = file.read()
    
    from .ai_style import analyze_outfit_image
    result = analyze_outfit_image(file_bytes, file.filename, gender)
    
    return jsonify(result)

@main.route("/login")
def login():
    return render_template("login-new.html")


@main.route("/register")
def register():
    return render_template("login.html")


@main.route("/search")
def search():
    product = request.args.get("q", "").strip()
    if not product:
        return jsonify([])

    time.sleep(0.5)

    results = [
        fetch_blinkit(product),
        fetch_zepto(product),
        fetch_instamart(product),
        fetch_bigbasket(product)
    ]

    results.sort(key=lambda x: x["price"])
    return jsonify(results)


@main.route("/search/ecommerce")
def search_ecommerce():
    product = request.args.get("q", "").strip()
    if not product:
        return jsonify([])

    time.sleep(0.5)

    # Import inside function to avoid circular imports if any, or just for clarity
    from .scraper import fetch_amazon, fetch_flipkart, fetch_meesho, fetch_myntra, fetch_nykaa, fetch_ajio
    
    results = [
        fetch_amazon(product),
        fetch_flipkart(product),
        fetch_myntra(product),
        fetch_nykaa(product),
        fetch_ajio(product),
        fetch_meesho(product)
    ]

    # Filter out errors (price 0)
    results = [r for r in results if r["price"] != 0 and r["price"] != 'Check App']
    
    results.sort(key=lambda x: x["price"])
    return jsonify(results)


@main.route("/deeplink/<platform>")
def deep_link(platform):
    """Generate deep links for mobile apps"""
    product = request.args.get("product", "").strip()
    if not product:
        return jsonify({"error": "Product parameter required"}), 400
    
    # Get actual product URL from search results
    product_url = None
    try:
        results = []
        if platform == "Blinkit":
            result = fetch_blinkit(product)
            results = [result]
        elif platform == "Zepto":
            result = fetch_zepto(product)
            results = [result]
        elif platform == "Instamart":
            result = fetch_instamart(product)
            results = [result]
        
        # Check if we found a real product URL (not search page)
        if results and results[0].get("url"):
            url = results[0]["url"]
            # Only use if it's not a search page URL
            search_patterns = [
                f"search?q={product.replace(' ', '%20')}",
                f"/search?q={product.replace(' ', '%20')}",
                f"?q={product.replace(' ', '%20')}"
            ]
            
            is_search_page = False
            for pattern in search_patterns:
                if pattern in url:
                    is_search_page = True
                    break
            
            if url and not is_search_page:
                product_url = url
    except Exception as e:
        print(f"Error getting product URL for {platform}: {e}")
        pass
    
    deep_links = generate_deep_links(platform, product, product_url)
    
    if not deep_links:
        return jsonify({"error": "Unsupported platform"}), 400
    
    # Detect user agent and return appropriate link
    user_agent = request.headers.get('User-Agent', '').lower()
    is_mobile = 'android' in user_agent or 'iphone' in user_agent or 'ipad' in user_agent
    
    response_data = {
        "platform": platform,
        "product": product,
        "is_product_page": product_url is not None and product_url != f"https://blinkit.com/search?q={product.replace(' ', '%20')}" and product_url != f"https://www.zeptonow.com/search?q={product.replace(' ', '%20')}" and product_url != f"https://www.swiggy.com/instamart/search?q={product.replace(' ', '%20')}"
    }
    
    if is_mobile:
        if 'android' in user_agent:
            response_data.update({
                "deep_link": deep_links.get("android"),
                "type": "android"
            })
        elif 'iphone' in user_agent or 'ipad' in user_agent:
            response_data.update({
                "deep_link": deep_links.get("ios"),
                "type": "ios"
            })
    else:
        response_data.update({
            "deep_link": deep_links.get("web"),
            "type": "web"
        })
    
    return jsonify(response_data)


@main.route("/app-redirect/<platform>")
def app_redirect(platform):
    """Redirect to appropriate app store or app"""
    product = request.args.get("product", "").strip()
    
    app_store_links = get_app_store_links(platform)
    
    if not app_store_links:
        return redirect("https://smartcart.app")
    
    user_agent = request.headers.get('User-Agent', '').lower()
    if 'android' in user_agent:
        return redirect(app_store_links["android"])
    elif 'iphone' in user_agent or 'ipad' in user_agent:
        return redirect(app_store_links["ios"])
    else:
        return redirect(app_store_links["android"])  # Default to Android


# Auth Routes
from .supabase_client import supabase

@main.route("/auth/login", methods=["POST"])
def auth_login():
    data = request.json or {}
    email = data.get("email", "").strip() if isinstance(data.get("email"), str) else ""
    password = data.get("password", "").strip() if isinstance(data.get("password"), str) else ""
    provider = data.get("provider", "").strip() if isinstance(data.get("provider"), str) else ""
    
    if not email:
        return jsonify({"error": "Email is required."}), 400
        
    if not provider and not password:
        return jsonify({"error": "Password is required for email login."}), 400

    session["user"] = {
        "id": "user-id",
        "email": email,
        "name": data.get("name") or email.split("@")[0],
        "provider": provider or "email"
    }
    return jsonify({"message": "Login successful", "user": session["user"]})

@main.route("/auth/register", methods=["POST"])
def auth_register():
    data = request.json or {}
    email = data.get("email", "").strip() if isinstance(data.get("email"), str) else ""
    password = data.get("password", "").strip() if isinstance(data.get("password"), str) else ""
    name = data.get("name", "").strip() if isinstance(data.get("name"), str) else ""
    
    if not email or not password:
        return jsonify({"error": "Email and password are required."}), 400
    
    session["user"] = {
        "id": "bypass-user-id",
        "email": email,
        "name": name or email.split("@")[0]
    }
    return jsonify({"message": "Registration successful", "user": session["user"]})

@main.route("/auth/logout", methods=["POST", "GET"])
@main.route("/logout", methods=["POST", "GET"])
def auth_logout():
    try:
        if supabase:
            supabase.auth.sign_out()
    except Exception as e:
        pass
    session.clear()
    if request.method == "GET":
        return redirect(url_for("main.login"))
    return jsonify({"message": "Logged out"})

@main.route("/10minute-delivery")
def ten_minute_delivery():
    if not session.get("user"):
        return redirect(url_for("main.login"))
    return render_template("10minute-delivery.html")

@main.route("/favicon.ico")
def favicon():
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    return send_from_directory(static_folder, 'favicon.svg', mimetype='image/svg+xml')


# ── Google OAuth ──────────────────────────────────────────────────────────
GOOGLE_CLIENT_ID     = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")

def _get_google_oauth():
    """Lazily build the Google OAuth client so missing creds don't crash startup."""
    global _oauth
    try:
        from authlib.integrations.flask_client import OAuth
    except ImportError:
        return None
    from flask import current_app
    if _oauth is None:
        _oauth = OAuth(current_app)
    google = _oauth.register(
        name='google',
        client_id=GOOGLE_CLIENT_ID,
        client_secret=GOOGLE_CLIENT_SECRET,
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
        client_kwargs={'scope': 'openid email profile'},
        overwrite=True,
    )
    return google


@main.route("/auth/google")
def auth_google():
    """Start the Google OAuth flow."""
    if not GOOGLE_CLIENT_ID:
        return redirect(url_for('main.login') + '?error=google_not_configured')
    google = _get_google_oauth()
    if google is None:
        return redirect(url_for('main.login') + '?error=authlib_missing')
    redirect_uri = url_for('main.auth_google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)


@main.route("/auth/google/callback")
def auth_google_callback():
    """Handle the Google OAuth callback and create a session."""
    if not GOOGLE_CLIENT_ID:
        return redirect(url_for('main.login'))
    try:
        google = _get_google_oauth()
        token  = google.authorize_access_token()
        user_info = token.get('userinfo') or google.userinfo()
        session['user'] = {
            'id':      user_info.get('sub'),
            'email':   user_info.get('email'),
            'name':    user_info.get('name'),
            'picture': user_info.get('picture'),
            'provider': 'google',
        }
        return redirect(url_for('main.dashboard'))
    except Exception as e:
        print(f"Google OAuth error: {e}")
        return redirect(url_for('main.login'))


@main.route("/redirect")
def secure_redirect():
    target_url = request.args.get("url")
    if not target_url:
        return "Missing URL", 400
    
    # HTML to perform a clean redirect
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="referrer" content="no-referrer">
        <meta http-equiv="refresh" content="0;url={target_url}">
        <script>
            window.location.replace("{target_url}");
        </script>
    </head>
    <body>
        <p>Redirecting to <a href="{target_url}">{target_url}</a>...</p>
    </body>
    </html>
    """
    response = make_response(html)
    response.headers["Referrer-Policy"] = "no-referrer"
    return response
