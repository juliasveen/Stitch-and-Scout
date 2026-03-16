import requests
from config import EBAY_APP_ID, EBAY_CERT_ID
import base64

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
            error = body.get("error_description") or body.get("error") or str(body)
            return None, f"eBay auth failed: {error}"
        return token, None
    except Exception as e:
        return None, f"eBay auth exception: {str(e)}"

def fetch_comp_listings(brand, item_type, condition, limit=5):
    """
    Tries eBay Browse API first, falls back to Finding API (no marketplace
    deletion endpoint required) if Browse returns auth errors.
    Returns (results, error_message).
    """
    token, auth_error = get_oauth_token()

    # --- Primary: Browse API ---
    if token:
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
            items = body.get("itemSummaries", [])
            if items:
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
                if results:
                    return results, None
        except Exception:
            pass

    # --- Fallback: Finding API (no deletion endpoint required) ---
    try:
        query = f"{brand} {item_type}".strip()
        url = (
            "https://svcs.ebay.com/services/search/FindingService/v1"
            f"?OPERATION-NAME=findCompletedItems"
            f"&SERVICE-VERSION=1.0.0"
            f"&SECURITY-APPNAME={EBAY_APP_ID}"
            f"&RESPONSE-DATA-FORMAT=JSON"
            f"&keywords={requests.utils.quote(query)}"
            f"&itemFilter(0).name=SoldItemsOnly&itemFilter(0).value=true"
            f"&itemFilter(1).name=Condition&itemFilter(1).value=Used"
            f"&paginationInput.entriesPerPage={limit}"
            f"&sortOrder=EndTimeSoonest"
        )
        response = requests.get(url, timeout=8)
        body = response.json()
        items = (body
                 .get("findCompletedItemsResponse", [{}])[0]
                 .get("searchResult", [{}])[0]
                 .get("item", []))
        if items:
            results = []
            for item in items:
                try:
                    results.append({
                        "title":     item["title"][0],
                        "price":     float(item["sellingStatus"][0]["currentPrice"][0]["__value__"]),
                        "url":       item["viewItemURL"][0],
                        "condition": item.get("condition", [{}])[0].get("conditionDisplayName", ["Used"])[0],
                    })
                except Exception:
                    continue
            if results:
                return results, None
        return [], "No sold listings found for this item."
    except Exception as e:
        return [], f"eBay fetch failed: {str(e)}"