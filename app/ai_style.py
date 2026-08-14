import os
import io
import json
from PIL import Image

try:
    import google.generativeai as genai
except ImportError:
    genai = None

MOCK_RESPONSE_MALE = {
    "analysis": {
        "face_shape": "Oval",
        "body_type": "Athletic",
        "height_category": "Average",
        "shoulder_type": "Medium",
        "clothing_size": "M",
        "confidence": 92
    },
    "suggestions": {
        "casual": {
            "top": "Fitted V-neck or Henley t-shirt",
            "bottom": "Slim-fit dark wash jeans",
            "footwear": "White canvas sneakers"
        },
        "office": {
            "top": "Light blue Oxford button-down shirt",
            "bottom": "Navy flat-front chinos",
            "layer": "Charcoal grey tailored blazer (optional)",
            "footwear": "Brown leather loafers"
        },
        "party": {
            "top": "Black slim-fit patterned button-up",
            "bottom": "Black tailored trousers",
            "layer": "Leather or suede bomber jacket",
            "footwear": "Chelsea boots"
        },
        "traditional": {
            "top": "Silk blend tailored Kurta in emerald green",
            "bottom": "White churidar",
            "footwear": "Traditional mojaris"
        },
        "best_colors": ["Navy", "Charcoal", "Emerald Green", "Burgundy"],
        "avoid_list": ["Oversized baggy clothes", "Horizontal stripes", "Pale yellow"]
    },
    "search_queries": [
        "Slim fit navy blue formal shirt for men",
        "Athletic fit dark wash jeans",
        "Emerald green silk kurta for men",
        "Charcoal grey tailored blazer",
        "White canvas casual sneakers"
    ]
}

MOCK_RESPONSE_FEMALE = {
    "analysis": {
        "face_shape": "Heart",
        "body_type": "Slim",
        "height_category": "Average",
        "shoulder_type": "Narrow",
        "clothing_size": "S",
        "confidence": 91
    },
    "suggestions": {
        "casual": {
            "top": "White ribbed fitted crop top",
            "bottom": "High-waisted wide-leg light wash jeans",
            "footwear": "Chunky white sneakers"
        },
        "office": {
            "top": "Beige silk tie-neck blouse",
            "bottom": "Black tailored wide-leg trousers",
            "layer": "Camel colored trench coat or blazer",
            "footwear": "Black pointed-toe pumps"
        },
        "party": {
            "dress": "Fitted velvet midnight blue slip dress",
            "accessories": "Statement silver geometric earrings",
            "footwear": "Strappy stiletto heels"
        },
        "traditional": {
            "saree": "Rose gold sequin georgette saree",
            "blouse": "Sleeveless sweet-heart neck blouse",
            "accessories": "Pearl choker and jhumkas",
            "footwear": "Embellished metallic heels"
        },
        "best_colors": ["Rose Gold", "Midnight Blue", "Camel", "Emerald"],
        "avoid_list": ["Boxy oversized cuts", "Large bold floral prints", "Neon yellow"]
    },
    "search_queries": [
        "Beige silk tie-neck blouse for women",
        "High-waisted wide-leg jeans",
        "Rose gold sequin saree",
        "Velvet midnight blue slip dress",
        "Black pointed-toe pumps"
    ]
}

def analyze_outfit_image(file_bytes, filename, gender="Auto"):
    """
    Analyzes an image and returns outfit suggestions based on the user's 3 prompts.
    """
    gemini_key = os.environ.get("GEMINI_API_KEY", "")

    # Determine which mock response to show based on dropdown
    mock = MOCK_RESPONSE_FEMALE if (str(gender).lower() == "female") else MOCK_RESPONSE_MALE

    if not genai or not gemini_key:
        print("Using MOCK response because GEMINI_API_KEY is missing or google-generativeai is not installed.")
        return mock

    try:
        genai.configure(api_key=gemini_key)
        
        # We use vision powers
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        image = Image.open(io.BytesIO(file_bytes))

        # STEP 1: Strict Validation
        validation_prompt = "Analyze this image. Is there a human person (or at least a human face/body) clearly visible in this image? Answer strictly with the word YES or NO, and nothing else."
        val_response = model.generate_content([validation_prompt, image])
        val_text = val_response.text.strip().upper()
        
        if "NO" in val_text or "YES" not in val_text:
            return {
                "error": "Please upload a clear photo of a person. I cannot style animals, objects, cartoons, or landscapes!"
            }

        # STEP 2: Full Analysis (We know it's a person now)
        prompt = f"""
You are an expert AI fashion stylist and personal shopper. Answer strictly in JSON format.

GENDER HINT: {gender} (If "Auto", determine based on the image.)

🧠 Prompt 1 – Image Analysis:
Analyze uploaded image and return:
- Face shape (Round, Oval, Square, Heart, Diamond, Rectangle)
- Body type (Slim, Athletic, Average, Muscular, Plus-size)
- Height category (Short, Average, Tall)
- Shoulder type (Narrow, Medium, Broad)
- Estimated clothing size (S, M, L, XL)
Return a structured result with a confidence percentage (integer 0-100). Do not guess sensitive attributes unnecessarily.

👔 Prompt 2 – Outfit Suggestion Logic:
Based on detected attributes, suggest outfits for the detected gender (Male or Female).
For Male: Shirt type, T-shirt type, Pant type, Blazer (if suitable), Best colors, Avoid list.
For Female: Kurti type, Saree drape suggestion, Top style, Jeans type, Dress type, Best colors, Avoid list.

Also suggest complete looks for:
- Casual look
- Office look
- Party look
- Traditional look

🛍️ Prompt 3 – Smart Cart Product Mapping:
Convert your outfit suggestions into 5 searchable product keywords/queries for e-commerce integration.

Return ONLY JSON matching this exact structure:
{{
  "analysis": {{
    "face_shape": "...",
    "body_type": "...",
    "height_category": "...",
    "shoulder_type": "...",
    "clothing_size": "...",
    "confidence": 95
  }},
  "suggestions": {{
    "casual": {{"top": "..", "bottom": "..", "footwear": ".."}},
    "office": {{"top": "..", "bottom": "..", "layer": "..", "footwear": ".."}},
    "party": {{"top": "..", "bottom": "..", "footwear": ".."}},
    "traditional": {{"top": "..", "bottom": "..", "footwear": ".."}},
    "best_colors": ["color1", "color2"],
    "avoid_list": ["item1", "item2"]
  }},
  "search_queries": [
    "query 1", "query 2", "query 3", "query 4", "query 5"
  ]
}}
"""

        response = model.generate_content([prompt, image])
        text = response.text

        # Clean JSON markdown if model adds it
        if text.startswith("```json"):
            text = text[7:]
        if text.endswith("```"):
            text = text[:-3]
        if text.endswith("```\n"):
            text = text[:-4]

        parsed_data = json.loads(text.strip())
        return parsed_data

    except Exception as e:
        print(f"Error calling Gemini AI: {e}")
        return {
            "error": "Failed to analyze image using AI.",
            "details": str(e),
            "fallback": mock
        }
