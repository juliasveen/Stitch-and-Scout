# 🧵 Stitch & Scout

**An AI pricing tool for thrift & resale sellers.**

Pricing secondhand items is incredibly tedious and Goodwill overcharging is no help! One item can mean 15 open eBay tabs just to land on a number. Stitch & Scout cuts that down to a single photo upload.

Upload a photo, get a price. That's it.

**[→ Try it live](https://stitch-and-scout.streamlit.app/)** &nbsp;·&nbsp; Python · Streamlit · Gemini Vision · scikit-learn · eBay API

---

![Stitch & Scout Demo](assets/demo.gif)

---

## What it does

Drop in 1–3 photos of a clothing item (ideally one of the full item, one of the tag) and it:

- **Reads the label** using Gemini Vision — brand, type, material, size, condition, even the style era
- **Predicts a price** using a Random Forest model trained on ~2,300 real eBay records, calibrated per platform so it's not inflated
- **Shows live eBay comps** so you can see what the same item is actually selling for right now
- **Calculates your profit** if you enter what you paid — shows margin and ROI on the tag
- **Exports a PDF hang tag** you can print and physically attach to the item
- **Tracks your inventory** in a scrapbook sidebar with an analytics dashboard

---

## Tech

| | |
|---|---|
| Frontend | Streamlit with a fully custom CSS theme (scrapbook aesthetic, fun fonts, washi-tape buttons) |
| Vision | Gemini 2.5 Flash Lite — reads tags, logos, stitching, hardware |
| Pricing model | scikit-learn Random Forest in a Pipeline, with a calibration chain that corrects for eBay listing inflation |
| Market data | eBay Browse API + Finding API fallback for live comp listings |
| PDF export | ReportLab — A6 hang tag with condition badge, profit summary, platform |
| Data | pandas, joblib |

---

## How pricing works

eBay listing prices run about 40–60% higher than what things actually sell for. The model corrects for this:

```
final_price = model_prediction
            × 0.62  (listing → sell price correction)
            × platform multiplier  (flea market = 0.70, eBay = 1.00)
            × condition multiplier (well-loved = 0.55, new with tags = 1.10)
```

Then clamped with per-condition floors and ceilings so nothing comes out at $0 or $200 for a used t-shirt.

---

## Run it locally

```bash
git clone https://github.com/juliasveen/Stitch-and-Scout.git
cd Stitch-and-Scout
pip install -r requirements.txt
```

Create a `.env` file:
```
GOOGLE_API_KEY=your_key
EBAY_APP_ID=your_key
EBAY_CERT_ID=your_key
```

Keys are free:
- Gemini → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)
- eBay → [developer.ebay.com](https://developer.ebay.com)

```bash
streamlit run main.py
```

To retrain the pricing model on fresh eBay data:
```bash
python sync_market.py
```

---

## Project structure

```
Stitch-and-Scout/
├── main.py              # app UI and page logic
├── style.py             # custom CSS theme + HTML components
├── config.py            # env variable loading (local + Streamlit Cloud)
├── sync_market.py       # eBay scraper + model retraining pipeline
└── utils/
    ├── vision_helper.py  # Gemini image analysis + JSON parsing
    ├── predictor.py      # price prediction + calibration
    ├── ebay_comps.py     # live eBay comp fetcher
    ├── tag_pdf.py        # PDF hang tag generator
    └── model_utils.py    # model retraining logic
```

---

## Roadmap

- [ ] Batch mode — price a whole pile at once
- [ ] Depop / Poshmark direct listing
- [ ] Vintage/Y2K era premium multiplier
- [ ] Mobile layout

---

*Built by [Julia Sveen](https://github.com/juliasveen) · [LinkedIn](https://www.linkedin.com/in/julia-sveen/)*