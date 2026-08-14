import random
import re

def get_estimated_price(product_name):
    """Generate estimated price based on current Indian market rates (Jan 2025)"""
    product_lower = product_name.lower().strip()
    
    # --- 1. QUANTITY PARSING ---
    # Attempt to find quantity multiplier (e.g. 500g = 0.5kg, 2l = 2x)
    quantity_multiplier = 1.0
    
    # Check for kg/g
    kg_match = re.search(r'(\d+(?:\.\d+)?)\s*kg', product_lower)
    g_match = re.search(r'(\d+)\s*g(?![a-z])', product_lower) # exclude 'gb' for electronics
    
    # Check for l/ml
    l_match = re.search(r'(\d+(?:\.\d+)?)\s*l(?![a-z])', product_lower)
    ml_match = re.search(r'(\d+)\s*ml', product_lower)
    
    # Check for pieces/pack
    pc_match = re.search(r'(\d+)\s*(?:pc|pcs|pack)', product_lower)

    if kg_match:
        quantity_multiplier = float(kg_match.group(1))
    elif g_match:
        quantity_multiplier = float(g_match.group(1)) / 1000.0
    elif l_match:
        quantity_multiplier = float(l_match.group(1))
    elif ml_match:
        quantity_multiplier = float(ml_match.group(1)) / 1000.0
    elif pc_match:
         # For pieces, we assume base price is usually for 1 unit or a standard pack
         # If > 1, we might scale, but often "pack of 6" is a distinct item type.
         # We'll apply a mild scaling if it's explicitly stated, but cap it.
         count = int(pc_match.group(1))
         if count > 1:
             quantity_multiplier = count * 0.8 # Bulk discount simulated

    # Normalize multiplier to avoid extreme values (e.g. 100g shouldn't be 0.1 of a standard packet price if standard is small)
    # We'll use this primarily for bulk items (rice, flour, oil).
    
    
    # --- 2. EXTENDED BASE PRICES (Unit Price usually for 1kg/1L/1 Unit) ---
    base_prices = {
        # Dairy & Fridge
        'milk': 56, 'curd': 90, 'dahi': 90, 'yogurt': 100,
        'paneer': 450, 'butter': 600, 'cheese': 600,
        'cream': 250, 'lassi': 40,
        
        # Staples (Per Kg/L)
        'bread': 45, 'atta': 45, 'flour': 45, 'rice': 70, 'basmati': 140,
        'dal': 130, 'toor': 140, 'moong': 120, 'masoor': 100,
        'sugar': 44, 'salt': 25, 'oil': 160, 'ghee': 650,
        'poha': 60, 'suji': 50, 'rava': 50, 'besan': 90,
        
        # Veggies (Per Kg)
        'onion': 50, 'potato': 40, 'tomato': 60,
        'capsicum': 80, 'carrot': 60, 'cucumber': 40,
        'peas': 120, 'mushroom': 400, # usually 200g packs, handled by logic
        'ginger': 120, 'garlic': 200, 'chilli': 100,
        'lemon': 150, 'coriander': 200, 'mint': 100,
        
        # Fruits (Per Kg/Unit)
        'apple': 200, 'banana': 60, 'orange': 100,
        'grapes': 120, 'papaya': 50, 'pomegranate': 180,
        'mango': 150, 'watermelon': 30, 'pineapple': 80,
        'coconut': 40, 'kiwi': 400,
        
        # Non-Veg
        'egg': 7, 'eggs': 7, # Per piece logic handled below
        'chicken': 260, 'mutton': 800, 'fish': 400,
        'prawns': 600,
        
        # Snacks & Beverages
        'coke': 90, 'pepsi': 90, 'sprite': 90, 'thums up': 90, # 2L implied usually, scaled down for match
        'chips': 40, 'biscuit': 30, 'cookie': 100,
        'chocolate': 100, 'maggi': 25, 'noodles': 30,
        'tea': 400, 'coffee': 1500, # Per kg implied
        'juice': 120, 'soda': 20,
        
        # Personal & Home
        'soap': 45, 'shampoo': 350, 'paste': 150, 'detergent': 150,
        'cleaner': 200, 'tissue': 60, 'diaper': 15, # per piece usually
    }

    # --- 3. HIGH VALUE TECH LOGIC ---
    if any(k in product_lower for k in ['iphone', 'galaxy s', 'macbook', 'laptop', 'ipad', 'pixel']):
        if 'iphone' in product_lower:
            base = 75000
            if 'pro' in product_lower: base += 40000
            if 'max' in product_lower: base += 10000
            if '14' in product_lower: base -= 20000
            if '13' in product_lower: base -= 30000
            return base
        if 's2' in product_lower and 'ultra' in product_lower: return 110000 # S23/S24 Ultra
        if 'macbook' in product_lower:
            return 140000 if 'pro' in product_lower else 90000
        if 'laptop' in product_lower: return 45000
        if 'ipad' in product_lower: 
            return 80000 if 'pro' in product_lower else 35000
            
    # --- 4. ACCESSORIES & ELECTRONICS ---
    if 'watch' in product_lower: return 25000 if 'apple' in product_lower or 'samsung' in product_lower else 3000
    if 'buds' in product_lower or 'airpods' in product_lower: return 15000 if 'pro' in product_lower else 4000
    if 'headphone' in product_lower: return 8000 if 'sony' in product_lower or 'bose' in product_lower else 2000
    
    # --- 5. CATEGORY SPECIFIC SCALING & MATCHING ---
    best_match_price = None
    best_match_len = 0
    
    for key, price in base_prices.items():
        if key in product_lower:
            if len(key) > best_match_len: # Find most specific match
                best_match_price = price
                best_match_len = len(key)

    if best_match_price:
        final_price = best_match_price
        
        # Apply quantity multiplier if reasonable
        # We don't linearly scale everything (e.g. 10g saffron != 10/1000 * wheat price)
        # But for 'milk 500ml' vs 'milk', it makes sense.
        if quantity_multiplier != 1.0:
            if quantity_multiplier < 0.1: # Small packs usually have premium
                final_price = final_price * quantity_multiplier * 2.5 
            elif quantity_multiplier < 1.0:
                final_price = final_price * quantity_multiplier * 1.2 # Small overhead
            else:
                final_price = final_price * quantity_multiplier
        
        # Pack of X logic
        if 'pack of' in product_lower or ' x ' in product_lower:
             # Heuristic bump if we missed the explicit number
             if quantity_multiplier == 1.0:
                 final_price *= 2.5
        
        return int(final_price)

    # --- 6. FALLBACK LOGIC ---
    # Try to guess category from words
    words = product_lower.split()
    
    if any(w in product_lower for w in ['shirt', 'pant', 'jeans', 'top', 'dress']):
        return random.randint(500, 2000)
    
    if any(w in product_lower for w in ['shoe', 'sneaker', 'sandal']):
        return random.randint(1000, 4000)

    # If it looks like a small quantity grocery item
    if 'kg' in product_lower or 'g' in product_lower or 'ml' in product_lower:
        return random.randint(50, 300)

    return random.randint(50, 500)
