import joblib
import pandas as pd

# eBay listing data skews ~40-60% above what items actually sell for
# on mixed platforms (Depop, Poshmark, flea markets, local).
# This corrects for that inflation.
MARKET_CALIBRATION = 0.62

# Per-platform adjustment if you want to fine-tune later
PLATFORM_MULTIPLIERS = {
    "Depop / Vinted":   0.85,
    "Poshmark":         0.90,
    "eBay":             1.00,
    "Flea Market":      0.70,
    "Mix of places":    0.80,
}

# Condition also affects realistic sell price beyond what the model sees
CONDITION_ADJUSTMENTS = {
    "New with Tags": 1.10,
    "Like New":      1.00,
    "Gently Used":   0.82,
    "Well-Loved":    0.55,
}

def predict_price(brand, item_type, condition, size, material, platform="Mix of places"):
    try:
        model = joblib.load("price_model.pkl")
        input_data = pd.DataFrame([{
            "brand":     str(brand).strip().lower(),
            "type":      str(item_type).strip().lower(),
            "condition": str(condition).strip(),
            "size":      str(size).strip(),
            "material":  str(material).strip()
        }])

        raw = float(model.predict(input_data)[0])

        # Apply calibration chain
        platform_mult  = PLATFORM_MULTIPLIERS.get(platform, 0.80)
        condition_mult = CONDITION_ADJUSTMENTS.get(condition, 0.82)
        calibrated     = raw * MARKET_CALIBRATION * platform_mult * condition_mult

        # Hard floor/ceiling per condition so prices stay sane
        floors   = {"New with Tags": 12, "Like New": 8, "Gently Used": 5, "Well-Loved": 3}
        ceilings = {"New with Tags": 120, "Like New": 80, "Gently Used": 50, "Well-Loved": 25}
        floor   = floors.get(condition, 5)
        ceiling = ceilings.get(condition, 50)

        return round(max(floor, min(ceiling, calibrated)), 2)

    except Exception:
        return 0