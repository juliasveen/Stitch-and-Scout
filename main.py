import streamlit as st
from PIL import Image
import pandas as pd
import os
import datetime
from dotenv import load_dotenv
from utils.vision_helper import analyze_multiple_images
from utils.predictor import predict_price
from utils.ebay_comps import fetch_comp_listings
from utils.tag_pdf import generate_tag_pdf
import style
from PIL import Image

load_dotenv()


icon = Image.open("icon.png")
st.set_page_config(page_title="Stitch & Scout", page_icon=icon, layout="wide")
style.apply_diy_theme()

# --- SESSION STATE ---
for key in ['detected', 'show_tag', 'last_price', 'last_name',
            'last_condition', 'last_type', 'last_cost', 'last_platform',
            'last_notes', 'last_brand', 'confirm_clear']:
    if key not in st.session_state:
        st.session_state[key] = None
st.session_state.setdefault('show_tag', False)
st.session_state.setdefault('confirm_clear', False)

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    tab_scrap, tab_stats = st.tabs(["📔 Scrapbook", "📊 Analytics"])

    with tab_scrap:
        if os.path.exists("saved_searches.csv"):
            df_saved = pd.read_csv("saved_searches.csv")
            st.caption(f"{len(df_saved)} item(s) saved")
            for _, row in df_saved.iloc[::-1].head(10).iterrows():
                st.markdown(
                    style.scrapbook_entry_html(row['Item'], row['Price'], row['Date']),
                    unsafe_allow_html=True
                )
            st.markdown("---")
            st.download_button(
                "📥 Export scrapbook CSV",
                data=df_saved.to_csv(index=False).encode(),
                file_name="stitch_scout_inventory.csv",
                mime="text/csv"
            )
            st.markdown("")
            if not st.session_state['confirm_clear']:
                if st.button("🗑️ Clear scrapbook"):
                    st.session_state['confirm_clear'] = True
                    st.rerun()
            else:
                st.warning("Are you sure? This cannot be undone.")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Yes, clear"):
                        os.remove("saved_searches.csv")
                        st.session_state['confirm_clear'] = False
                        st.rerun()
                with c2:
                    if st.button("Cancel"):
                        st.session_state['confirm_clear'] = False
                        st.rerun()
        else:
            st.caption("No saved items yet. Generate a tag to get started!")

    with tab_stats:
        if os.path.exists("saved_searches.csv"):
            df_stats = pd.read_csv("saved_searches.csv")
            df_stats['price_val'] = pd.to_numeric(
                df_stats['Price'].astype(str).str.replace('$','',regex=False).str.strip(),
                errors='coerce')
            df_stats = df_stats.dropna(subset=['price_val'])

            st.metric("Total inventory value", f"${df_stats['price_val'].sum():.2f}")
            st.metric("Average price",         f"${df_stats['price_val'].mean():.2f}")
            st.metric("Items logged",          len(df_stats))

            if 'Cost' in df_stats.columns:
                df_stats['cost_val'] = pd.to_numeric(
                    df_stats['Cost'].astype(str).str.replace('$','',regex=False),
                    errors='coerce')
                total_cost   = df_stats['cost_val'].sum()
                total_profit = (df_stats['price_val'] - df_stats['cost_val']).sum()
                roi_pct      = (total_profit / total_cost * 100) if total_cost > 0 else 0
                st.metric("Est. total profit", f"${total_profit:.2f}",
                          delta=f"{roi_pct:.0f}% ROI")

            if 'Date' in df_stats.columns:
                df_stats['Date'] = pd.to_datetime(df_stats['Date'], errors='coerce')
                chart_df = (df_stats.dropna(subset=['Date'])
                            .sort_values('Date')
                            .set_index('Date')[['price_val']]
                            .rename(columns={'price_val': 'Price ($)'}))
                if not chart_df.empty:
                    st.caption("Prices over time")
                    st.line_chart(chart_df, height=160)

            if 'Item' in df_stats.columns:
                df_stats['brand'] = df_stats['Item'].str.split().str[0]
                top_brands = (df_stats.groupby('brand')['price_val']
                              .mean().sort_values(ascending=False).head(5))
                if not top_brands.empty:
                    st.caption("Top brands by avg. price")
                    st.bar_chart(top_brands, height=160)
        else:
            st.caption("Save some items first to see analytics!")

# ── MAIN ──────────────────────────────────────────────────────────────────────
st.title("🧵 STITCH & SCOUT")

uploaded_files = st.file_uploader(
    "PIN PHOTOS — upload the full item + any label/tag photos for best results",
    accept_multiple_files=True,
    type=["jpg", "jpeg", "png", "heic", "webp"]
)

if uploaded_files:
    imgs = [Image.open(f) for f in uploaded_files]
    st.image(imgs, width=250)
    st.caption(f"📎 {len(imgs)} photo(s) pinned — include a tag/label shot for brand accuracy!")

    if st.button("✨ START SCAN"):
        with st.spinner("Scanning photos... reading tags and labels..."):
            st.session_state['detected'] = analyze_multiple_images(imgs)
            st.session_state['show_tag'] = False

# ── ITEM DETAILS FORM ─────────────────────────────────────────────────────────
if st.session_state['detected']:
    d = st.session_state['detected']
    confidence = d.get('confidence', 'low')

    conf_icons  = {"high": "🟢", "medium": "🟡", "low": "🔴"}
    conf_labels = {
        "high":   "High confidence — tags clearly visible",
        "medium": "Medium confidence — partially visible",
        "low":    "Low confidence — please review all fields",
    }
    st.markdown(f"{conf_icons[confidence]} **Scan confidence:** {conf_labels[confidence]}")

    if d.get('notes'):
        st.info(f"💡 **Scout's note:** {d['notes']}")

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        brand     = st.text_input("BRAND",    value=d.get('brand', 'Unknown'),
                       help="Detected from label/logo. Edit if incorrect.")
        item_type = st.text_input("TYPE",     value=d.get('type', 'Item'))
        color     = st.text_input("COLOR",    value=d.get('color', ''))
        style_era = st.text_input("ERA / STYLE", value=d.get('style_era', 'Contemporary'))
        cost_paid = st.number_input("WHAT DID YOU PAY? ($)",
                       min_value=0.0, max_value=500.0, value=0.0, step=0.50,
                       help="Enter your purchase cost to see profit & ROI on the tag")

    with col2:
        condition_options = ["Gently Used", "New with Tags", "Like New", "Well-Loved"]
        condition_hint    = d.get('condition_hint', 'Gently Used')
        default_cond_idx  = condition_options.index(condition_hint) if condition_hint in condition_options else 0
        condition = st.selectbox("CONDITION", condition_options, index=default_cond_idx,
                       help="Pre-filled from scan — double-check this one!")

        size_options = ["XS", "S", "M", "L", "XL", "OS"]
        size_hint    = d.get('size_hint', 'Not visible')
        default_size = "M"
        for s in size_options:
            if s.upper() in size_hint.upper():
                default_size = s
                break
        size = st.selectbox("SIZE", size_options, index=size_options.index(default_size))

        material = st.text_input("MATERIAL", value=d.get('material', 'Unknown'))
        platform = st.selectbox("SELLING ON",
                       ["Mix of places", "Depop / Vinted", "Poshmark", "eBay", "Flea Market"],
                       help="Prices are calibrated per platform")
        strategy = st.select_slider("PRICING STRATEGY",
                       options=["Quick Flip", "Market Rate", "Boutique"],
                       value="Market Rate",
                       help="Quick Flip = −30% · Market Rate = fair value · Boutique = +35%")

    if st.button("🏷️ GENERATE TAG"):
        base = predict_price(brand, item_type, condition, size, material, platform)
        if base == 0:
            st.warning("⚠️ Price model not trained yet — showing condition-based estimate.")
            fallback = {"New with Tags": 22, "Like New": 18, "Gently Used": 12, "Well-Loved": 6}
            base = fallback.get(condition, 12)

        strat_map   = {"Quick Flip": 0.70, "Market Rate": 1.0, "Boutique": 1.35}
        final_price = round(base * strat_map.get(strategy, 1.0), 2)

        st.session_state.update({
            'last_price':     final_price,
            'last_name':      f"{brand} {item_type}",
            'last_type':      item_type,
            'last_condition': condition,
            'last_cost':      cost_paid,
            'last_platform':  platform,
            'last_brand':     brand,
            'last_notes':     d.get('notes', ''),
            'show_tag':       True,
        })

# ── HANG TAG + ACTIONS ────────────────────────────────────────────────────────
if st.session_state.get('show_tag') and st.session_state.get('last_price'):
    price     = st.session_state['last_price']
    cost      = st.session_state.get('last_cost') or 0.0
    name      = st.session_state['last_name']
    item_type = st.session_state.get('last_type', '')
    condition = st.session_state.get('last_condition', 'Gently Used')
    platform  = st.session_state.get('last_platform', '')
    notes     = st.session_state.get('last_notes', '')
    brand     = st.session_state.get('last_brand', '')

    st.markdown("---")
    tag_col, info_col = st.columns([1, 1])

    with tag_col:
        st.markdown(
            style.hang_tag_html(name, item_type, price, condition),
            unsafe_allow_html=True
        )

        # Profit strip
        if cost > 0:
            profit = price - cost
            roi    = (profit / cost * 100)
            p_color = "#3b6d11" if profit >= 0 else "#802b2b"
            st.markdown(
                f"""<div style="margin-top:12px; padding:12px 16px;
                    background:#f0f7e8; border-radius:12px; border:1px solid #b5c99a;
                    font-family:'Courier New',monospace;">
                    <span style="color:#5d1a1a">Paid: <strong>${cost:.2f}</strong></span>
                    &nbsp;&nbsp;
                    <span style="color:{p_color}">
                        Est. profit: <strong>${profit:.2f}</strong>
                        &nbsp;({roi:.0f}% ROI)
                    </span>
                </div>""",
                unsafe_allow_html=True
            )

    with info_col:
        st.markdown("#### Actions")
        btn1, btn2 = st.columns(2)

        with btn1:
            if st.button("💾 Save to scrapbook"):
                new_row = pd.DataFrame([{
                    "Item":  name,
                    "Price": f"${price:.2f}",
                    "Cost":  f"${cost:.2f}" if cost > 0 else "",
                    "Date":  datetime.date.today().strftime("%Y-%m-%d"),
                }])
                if os.path.exists("saved_searches.csv"):
                    existing = pd.read_csv("saved_searches.csv")
                    updated  = pd.concat([existing, new_row], ignore_index=True)
                else:
                    updated = new_row
                updated.to_csv("saved_searches.csv", index=False)
                st.success("✅ Saved!")
                st.rerun()

        with btn2:
            pdf_bytes = generate_tag_pdf(
                item_name=name,
                item_type=item_type,
                price=price,
                condition=condition,
                cost_paid=cost,
                platform=platform,
                notes=notes,
            )
            st.download_button(
                "🖨️ Download PDF tag",
                data=pdf_bytes,
                file_name=f"{name.replace(' ', '_')}_tag.pdf",
                mime="application/pdf",
            )

        # Comp listings
        st.markdown("#### 🔍 eBay comp listings")
        with st.spinner("Fetching live comps..."):
            comps, comp_error = fetch_comp_listings(brand, item_type, condition, limit=5)

        if comps:
            prices    = [c['price'] for c in comps]
            avg_comp  = sum(prices) / len(prices)
            delta     = price - avg_comp
            direction = "above" if delta >= 0 else "below"
            delta_color = "#3b6d11" if delta <= 0 else "#802b2b"
            st.markdown(
                f'''<div style="display:flex;gap:16px;align-items:center;
                    padding:10px 14px;margin-bottom:10px;
                    background:#fdfaf0;border:1px solid #d4a373;border-radius:10px;
                    font-family:'Courier New',monospace;">
                    <div>
                        <div style="font-size:10px;color:#888;text-transform:uppercase;letter-spacing:0.05em;">eBay avg</div>
                        <div style="font-size:20px;font-weight:bold;color:#802b2b;">${avg_comp:.2f}</div>
                    </div>
                    <div style="font-size:18px;color:#d4a373;">·</div>
                    <div>
                        <div style="font-size:10px;color:#888;text-transform:uppercase;letter-spacing:0.05em;">Your price</div>
                        <div style="font-size:20px;font-weight:bold;color:#802b2b;">${price:.2f}</div>
                    </div>
                    <div style="margin-left:auto;padding:4px 10px;border-radius:20px;
                        background:{delta_color};color:white;font-size:11px;font-weight:bold;">
                        ${abs(delta):.2f} {direction} market
                    </div>
                </div>''',
                unsafe_allow_html=True
            )
            for comp in comps:
                st.markdown(
                    f"""<div style="padding:8px 10px; margin-bottom:6px;
                        border:1px solid #d4a373; border-radius:10px;
                        background:#fdfaf0; font-family:'Courier New',monospace;">
                        <div style="font-size:12px;color:#333;">
                            {comp['title'][:65]}...
                        </div>
                        <div style="display:flex;justify-content:space-between;margin-top:4px;">
                            <span style="font-size:11px;color:#802b2b;">{comp['condition']}</span>
                            <strong style="color:#802b2b;">${comp['price']:.2f}</strong>
                        </div>
                        <a href="{comp['url']}" target="_blank"
                           style="font-size:10px;color:#802b2b;">View on eBay →</a>
                    </div>""",
                    unsafe_allow_html=True
                )
        else:
            st.warning(f"⚠️ {comp_error}" if comp_error else "No comps found.")