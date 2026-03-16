# 🧵 Stitch & Scout
### AI-Powered Resale Pricing Tool for Thrift & Secondhand Sellers

> Upload a photo of any clothing item. Stitch & Scout identifies the brand, detects condition, predicts a calibrated resale price, and validates it against live eBay listings — all in under 10 seconds.

**[🚀 Live Demo →](https://stitch-and-scout.streamlit.app/)** &nbsp;|&nbsp; Built with Python · Streamlit · Gemini Vision · scikit-learn · eBay API

---

![Stitch & Scout Demo](assets/demo.gif)

---

## What it does

Resale sellers waste hours manually researching prices across Depop, Poshmark, and eBay. Stitch & Scout automates the entire workflow — from photo to printable price tag — in one tool.

| Step | What happens |
|---|---|
| 📸 **Scan** | Upload 1–3 photos. Gemini Vision reads labels, logos, and fabric tags to detect brand, type, material, condition, size, and era |
| 🏷️ **Price** | A Random Forest model trained on ~2,300 eBay records predicts a base price, then applies platform and condition calibration multipliers |
| 🔍 **Validate** | Live eBay comp listings show 5 current listings for the same item so you can sanity-check before pricing |
| 💰 **Profit** | Enter what you paid — the app calculates estimated profit and ROI instantly |
| 🖨️ **Export** | Download a print-ready A6 PDF hang tag or save the item to your scrapbook inventory |

---

## Features

- **AI vision scanning** — Gemini Vision API reads clothing tags and logos with high/medium/low confidence scoring
- **ML price prediction** — Random Forest Regressor trained on real eBay sold data, with platform-specific calibration (Depop vs. eBay vs. flea market)
- **Live eBay comps** — eBay Browse API fetches current listings and shows whether your price is above or below market
- **Profit & ROI calculator** — enter your purchase cost and see estimated margin on every item
- **PDF hang tag export** — print-ready A6 tags generated with ReportLab, including condition badge and profit summary
- **Scrapbook inventory** — save items, export your full inventory as CSV
- **Analytics dashboard** — total inventory value, average price, price-over-time chart, top brands by average price
- **Scrapbook-aesthetic UI** — custom Streamlit theme with handwritten fonts, warm palette, and washi-tape sidebar cards

---

## Tech stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit (custom CSS theme) |
| Vision AI | Google Gemini Vision API (`gemini-2.5-flash-lite`) |
| Price model | scikit-learn `RandomForestRegressor` in a `Pipeline` with `OneHotEncoder` |
| Training data | ~2,300 records scraped from eBay Browse API via OAuth2 |
| Market comps | eBay Browse API (live listings, real-time) |
| PDF generation | ReportLab (A6 hang tag layout) |
| Data | pandas, joblib |
| Config | python-dotenv |

---

## How the pricing works

Raw eBay listing data skews 40–60% above real sell prices. The predictor applies a calibration chain:

```
final_price = model_prediction
            × market_calibration (0.62)
            × platform_multiplier (0.70–1.00)
            × condition_multiplier (0.55–1.10)
```

Clamped by per-condition floors and ceilings so prices are always realistic for the secondhand market.

---

## Project structure

```
ai-thrift-finder/
├── main.py              # Streamlit app — UI and page logic
├── style.py             # Custom CSS theme and HTML components
├── config.py            # Environment variable loading
├── sync_market.py       # eBay data scraper + model retraining pipeline
├── dataset.csv          # Training data (~2,300 eBay records)
├── price_model.pkl      # Trained Random Forest model
└── utils/
    ├── vision_helper.py  # Gemini Vision API — image analysis + JSON parsing
    ├── predictor.py      # Price prediction + calibration logic
    ├── ebay_comps.py     # Live eBay comp listing fetcher
    ├── tag_pdf.py        # ReportLab PDF hang tag generator
    └── model_utils.py    # Model retraining utility
```

---

## Run locally

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/ai-thrift-finder.git
cd ai-thrift-finder
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up API keys**

Create a `.env` file in the project root:
```
GOOGLE_API_KEY=your_gemini_api_key
EBAY_APP_ID=your_ebay_app_id
EBAY_CERT_ID=your_ebay_cert_id
```

Get your keys:
- **Gemini** → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey) (free tier available)
- **eBay** → [developer.ebay.com](https://developer.ebay.com) (free developer account)

**4. Run**
```bash
streamlit run main.py
```

Opens at `http://localhost:8501`

**Optional: retrain the model on fresh data**
```bash
python sync_market.py   # pulls new eBay sold listings
```

---

## Screenshots

| Scan & detect | Hang tag + profit | Analytics dashboard |
|---|---|---|
| *(add screenshot)* | *(add screenshot)* | *(add screenshot)* |

---

## Roadmap

- [ ] Batch mode — price 10+ items from a single upload session
- [ ] Poshmark / Depop direct listing integration
- [ ] Style era premium pricing (vintage Y2K commands higher margins)
- [ ] Mobile-optimized layout

---

## Author

**Julia!** · [github.com/yourusername](https://github.com/yourusername) · [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)