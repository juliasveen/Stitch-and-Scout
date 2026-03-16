from google import genai
from google.genai import types
import json
import io
from config import GOOGLE_API_KEY

def analyze_multiple_images(image_list):
    """
    Analyzes clothing images using Gemini Vision (google-genai SDK).
    Returns a dict with detected brand, type, material, color, size_hint,
    condition_hint, and confidence ('high' | 'medium' | 'low').
    """
    client = genai.Client(api_key=GOOGLE_API_KEY)

    prompt = """You are an expert fashion authenticator and thrift store buyer with 15+ years of experience.
Examine these clothing item photo(s) carefully — including any visible tags, logos, labels, stitching, hardware, or print — and extract every detail you can.

Return ONLY a valid JSON object with these exact keys (no markdown, no explanation):

{
  "brand": "The brand name exactly as it appears on the label or logo. Look for tags on collar, cuffs, hem, waistband, interior lining. If a logo is visible (e.g. swoosh, polo player, crocodile), name that brand. Use 'Unknown' only if truly unidentifiable.",
  "type": "Specific garment type (e.g. 'Denim Jacket', 'Silk Slip Dress', 'Cargo Pants', 'Cashmere Crewneck'). Be specific.",
  "material": "Primary fabric/material. Look for care label or texture. Examples: '100% Cotton', 'Wool Blend', 'Polyester Satin', 'Genuine Leather'.",
  "color": "Primary color(s) of the item. Be descriptive: 'Washed Black', 'Cream', 'Burgundy Plaid'.",
  "size_hint": "Any visible size marking on tags. Return the value (e.g. 'M', '32W 30L', '8', 'OS') or 'Not visible'.",
  "condition_hint": "Your honest assessment based on what you see: 'New with Tags', 'Like New', 'Gently Used', or 'Well-Loved'. Note any visible wear, pilling, fading, or damage.",
  "style_era": "Estimated decade or era if detectable: 'Y2K', 'Vintage 90s', 'Contemporary', '80s Power Shoulder', etc.",
  "confidence": "Your overall confidence in this reading: 'high' if tags/logos clearly visible, 'medium' if partially visible, 'low' if guessing from texture/silhouette only.",
  "notes": "Any other resale-relevant details: limited edition, rare colorway, distressing details, hardware quality, country of manufacture, authentication markers, etc. Empty string if nothing notable."
}

Critical rules:
- If multiple images are provided, synthesize ALL of them. A label photo + a full-item photo together give you more data.
- Never hallucinate a brand. If you see a tag but can't read it clearly, say 'Unreadable tag' not a guess.
- For luxury brands (Gucci, Prada, Louis Vuitton, Burberry, etc.) look for authentication details: stitching quality, font precision, hardware weight, serial numbers.
- Return ONLY the JSON. No preamble, no markdown fences."""

    defaults = {
        "brand": "Unknown",
        "type": "Clothing Item",
        "material": "Unknown",
        "color": "Unknown",
        "size_hint": "Not visible",
        "condition_hint": "Gently Used",
        "style_era": "Contemporary",
        "confidence": "low",
        "notes": ""
    }

    try:
        # Convert PIL images to bytes parts for the new SDK
        parts = [prompt]
        for img in image_list:
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            parts.append(types.Part.from_bytes(
                data=buf.getvalue(),
                mime_type="image/jpeg"
            ))

        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=parts
        )
        raw = response.text.strip()

        # Strip markdown fences if model ignores instructions
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
            raw = raw.strip()

        parsed = json.loads(raw)
        result = {**defaults, **parsed}

        if result["confidence"] not in ("high", "medium", "low"):
            result["confidence"] = "medium"

        return result

    except json.JSONDecodeError:
        result = defaults.copy()
        result["notes"] = "Could not parse structured response. Please fill in details manually."
        result["confidence"] = "low"
        try:
            for line in raw.split('\n'):
                low = line.lower()
                if 'brand:' in low:
                    result['brand'] = line.split(':', 1)[-1].strip().strip('"').title()
                elif 'type:' in low:
                    result['type'] = line.split(':', 1)[-1].strip().strip('"').title()
                elif 'material:' in low:
                    result['material'] = line.split(':', 1)[-1].strip().strip('"').title()
        except Exception:
            pass
        return result

    except Exception as e:
        result = defaults.copy()
        result["notes"] = f"Scan error: {str(e)}"
        result["confidence"] = "low"
        return result