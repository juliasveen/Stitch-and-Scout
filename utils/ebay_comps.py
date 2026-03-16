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
        body = response.json()
        token = body.get("access_token")
        if not token:
            # Return error string so caller can surface it
            error = body.get("error_description") or body.get("error") or str(body)
            return None, f"eBay auth failed: {error}"
        return token, None
    except Exception as e:
        return None, f"eBay auth exception: {str(e)}"

def fetch_comp_listings(brand, item_type, condition, limit=5):
    """
    Returns (results, error_message).
    results = list of {title, price, url, condition}
    error_message = None if successful, string if failed.
    """
    token, auth_error = get_oauth_token()
    if not token:
        return [], auth_error

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
        body = response.json()

        # Surface any API-level errors
        if "errors" in body:
            msg = body["errors"][0].get("longMessage") or body["errors"][0].get("message", str(body))
            return [], f"eBay API error: {msg}"

        items = body.get("itemSummaries", [])
        if not items:
            return [], "No listings found for this item on eBay."

        results = []
        for item in items:
            try:
                results.append({
                    "title":     item.get("title", ""),
                    "price":     float(item["price"]["value"]),
                    "url":       item.get("itemWebUrl", "#"),
                    "condition": item.get("condition", "Used"),
                })
            except Exception:
                continue
        return results, None

    except Exception as e:
        return [], f"eBay fetch exception: {str(e)}"