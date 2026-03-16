import requests
import base64
from config import EBAY_APP_ID, EBAY_CERT_ID

def get_oauth_token():
    auth_str = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    encoded_auth = base64.b64encode(auth_str.encode()).decode()
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {encoded_auth}"
    }
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    try:
        response = requests.post(url, headers=headers, data=data, timeout=8)
        return response.json().get("access_token")
    except Exception:
        return None

def fetch_comp_listings(brand, item_type, condition, limit=5):
    """
    Returns up to `limit` live eBay listings for a given item.
    Each result: {title, price, url, condition, image_url}
    """
    token = get_oauth_token()
    if not token:
        return []

    query = f"{brand} {item_type}".strip()
    url = (
        f"https://api.ebay.com/buy/browse/v1/item_summary/search"
        f"?q={requests.utils.quote(query)}&limit={limit}"
        f"&filter=conditions%3A%7BUSED%7C%7CVERY_GOOD%7C%7CGOOD%7C%7CACCEPTABLE%7D"
    )
    headers = {
        "Authorization": f"Bearer {token}",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    try:
        response = requests.get(url, headers=headers, timeout=8)
        items = response.json().get("itemSummaries", [])
        results = []
        for item in items:
            try:
                results.append({
                    "title":     item.get("title", ""),
                    "price":     float(item["price"]["value"]),
                    "url":       item.get("itemWebUrl", "#"),
                    "condition": item.get("condition", "Used"),
                    "image_url": item.get("image", {}).get("imageUrl", ""),
                })
            except Exception:
                continue
        return results
    except Exception:
        return []