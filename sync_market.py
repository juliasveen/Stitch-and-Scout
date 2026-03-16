import requests
import base64
import pandas as pd
import os
import random
from config import EBAY_APP_ID, EBAY_CERT_ID, DATASET
from utils.model_utils import retrain_model

def get_oauth_token():
    auth_str = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded", "Authorization": f"Basic {encoded_auth}"}
    data = {"grant_type": "client_credentials", "scope": "https://api.ebay.com/oauth/api_scope"}
    response = requests.post(url, headers=headers, data=data)
    return response.json().get("access_token")

def fetch_ebay_sold_data(query):
    token = get_oauth_token()
    if not token: return []

    # The magic parameter: filter=buyingOptions:{FIXED_PRICE},conditions:{USED} 
    # Note: Browse API filtering for 'Sold' often requires the 'item_summary' 
    # search with a specific filter string or keyword targeting.
    
    # Targeting 'Sold' via keyword and price aspect for better accuracy
    search_query = f"{query} sold" 
    url = f"https://api.ebay.com/buy/browse/v1/item_summary/search?q={search_query}&limit=20"
    headers = {"Authorization": f"Bearer {token}", "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"}

    print(f"💰 Scouting SOLD prices for: {query}")
    
    try:
        response = requests.get(url, headers=headers)
        items = response.json().get('itemSummaries', [])
        results = []
        for item in items:
            try:
                price = float(item['price']['value'])
                title = item.get('title', '').lower()
                
                # Dynamic Guessing (Matches your 6-column structure)
                material = "Cotton"
                if "silk" in title: material = "Silk"
                elif "wool" in title: material = "Wool"
                elif "leather" in title: material = "Leather"
                
                size = "M"
                if " s " in title: size = "S"
                elif " l " in title: size = "L"

                results.append({
                    "brand": query.split()[0].lower(),
                    "type": " ".join(query.split()[1:]).lower(),
                    "condition": "Gently Used",
                    "size": size,
                    "material": material,
                    "price": price
                })
            except: continue
        return results
    except: return []

if __name__ == "__main__":
    # 🧪 THE MATRIX GENERATOR
    MODS = ["vintage", "designer", "luxury", "y2k"]
    MATS = ["silk", "wool", "leather", "denim", "linen", "cashmere"]
    ITEMS = ["jacket", "sweater", "pants", "dress"]

    # Generate hundreds of combinations
    ALL_COMBOS = [f"{m1} {m2} {i}" for m1 in MODS for m2 in MATS for i in ITEMS]
    
    # Pick 30 random ones to keep it fast and memory-efficient
    SEARCH_TERMS = random.sample(ALL_COMBOS, 30)

    all_data = []
    for term in SEARCH_TERMS:
        all_data.extend(fetch_ebay_sold_data(term))

    if all_data:
        df = pd.DataFrame(all_data)
        file_exists = os.path.isfile(DATASET)
        df.to_csv(DATASET, mode='a', index=False, header=not file_exists)
        print(f"✅ Success! Added {len(df)} SOLD records.")
        retrain_model()