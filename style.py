import streamlit as st

def apply_diy_theme():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&family=Fira+Sans:wght@400;700&display=swap');

    /* ── Remove default Streamlit top padding so banner touches the top ── */
    #root > div:first-child { padding-top: 0 !important; }
    .stApp > header { display: none !important; }
    .block-container {
        padding-top: 0 !important;
        padding-bottom: 2rem !important;
    }

    /* ── Layered DIY background ── */
    .stApp {
        background-color: #fdf6ee;
        background-image:
            /* Pink gingham grid */
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 38px,
                rgba(255, 182, 193, 0.25) 38px,
                rgba(255, 182, 193, 0.25) 40px
            ),
            repeating-linear-gradient(
                90deg,
                transparent,
                transparent 38px,
                rgba(255, 182, 193, 0.25) 38px,
                rgba(255, 182, 193, 0.25) 40px
            ),
            /* Sage green diagonal stripes underneath */
            repeating-linear-gradient(
                45deg,
                transparent,
                transparent 18px,
                rgba(181, 201, 154, 0.12) 18px,
                rgba(181, 201, 154, 0.12) 20px
            );
        background-attachment: fixed;
    }

    /* ── Sticky maroon banner — flush to top ── */
    h1 {
        font-family: 'Gaegu', cursive !important;
        background-color: #802b2b !important;
        color: #fce4ec !important;
        padding: 22px 20px 28px !important;
        margin: 0 0 28px 0 !important;
        border-radius: 0 !important;
        text-align: center !important;
        border-bottom: 6px solid #d4a373 !important;
        box-shadow: 0 6px 0 #5d1a1a, 0 10px 20px rgba(90,20,20,0.18) !important;
        position: relative;
        letter-spacing: 0.04em;
    }

    /* Scallop edge on banner using pseudo-element */
    h1::after {
        content: '';
        position: absolute;
        bottom: -18px;
        left: 0;
        right: 0;
        height: 18px;
        background:
            radial-gradient(circle at 10px -2px, transparent 12px, #802b2b 13px) left/20px 18px,
            radial-gradient(circle at 10px -2px, transparent 12px, #d4a373 13px) left/20px 18px;
        background-repeat: repeat-x;
        background-position: 0 0, 0 2px;
    }

    /* ── Decorative corner scissors on banner ── */
    h1::before {
        content: '✂ ✂';
        position: absolute;
        top: 50%;
        right: 24px;
        transform: translateY(-50%);
        font-size: 20px;
        opacity: 0.4;
        letter-spacing: 8px;
    }

    /* ── Typography ── */
    h2, h3 {
        font-family: 'Gaegu', cursive !important;
        color: #5d1a1a !important;
    }

    label, p, .stCaption {
        font-family: 'Gaegu', cursive !important;
        color: #5d1a1a !important;
    }

    /* ── Sidebar: torn paper edge ── */
    [data-testid="stSidebar"] {
        background-color: #fff8f0 !important;
        border-right: 3px solid #e8c9a0 !important;
        background-image:
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 24px,
                rgba(212,163,115,0.15) 24px,
                rgba(212,163,115,0.15) 25px
            );
    }

    /* ── Washi tape buttons ── */
    .stButton > button {
        background-color: #b5c99a !important;
        color: #3a3a2a !important;
        border: none !important;
        border-bottom: 4px solid #869471 !important;
        border-radius: 0px !important;
        font-family: 'Gaegu', cursive !important;
        font-weight: 700 !important;
        font-size: 20px !important;
        transform: rotate(-1deg);
        transition: all 0.18s ease;
        box-shadow: 2px 2px 0 #869471;
    }
    .stButton > button:hover {
        transform: rotate(1deg) scale(1.04);
        background-color: #ffb7b2 !important;
        box-shadow: 3px 3px 0 #d4807a;
    }

    /* ── Crafty input boxes ── */
    input, textarea, div[data-baseweb="select"] {
        background-color: #fffdf7 !important;
        border: 2px solid #d4a373 !important;
        border-radius: 10px !important;
        color: #5d1a1a !important;
        font-family: 'Gaegu', cursive !important;
    }

    /* ── Hang tag card ── */
    .hang-tag {
        background: #fdfaf0;
        border: 4px solid #802b2b;
        padding: 30px;
        border-radius: 20px;
        position: relative;
        box-shadow: 8px 8px 0px #b5c99a;
        background-image:
            radial-gradient(circle, rgba(212,163,115,0.08) 1px, transparent 1px);
        background-size: 16px 16px;
    }
    .hang-tag::before {
        content: "●";
        position: absolute;
        top: 10px;
        left: 50%;
        color: #802b2b;
        font-size: 14px;
    }

    /* ── Streamlit tab styling ── */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        font-family: 'Gaegu', cursive !important;
        font-size: 16px !important;
        color: #802b2b !important;
    }

    /* ── Download button matches washi style ── */
    .stDownloadButton > button {
        background-color: #ffb7b2 !important;
        color: #5d1a1a !important;
        border: none !important;
        border-bottom: 4px solid #d4807a !important;
        border-radius: 0px !important;
        font-family: 'Gaegu', cursive !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        transform: rotate(1deg);
        transition: all 0.18s ease;
    }
    .stDownloadButton > button:hover {
        transform: rotate(-1deg) scale(1.04);
        background-color: #b5c99a !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        border: 3px dashed #d4a373 !important;
        border-radius: 16px !important;
        background: rgba(253,250,240,0.7) !important;
        padding: 10px !important;
    }

    </style>
    """, unsafe_allow_html=True)


def hang_tag_html(brand, item_type, price, condition):
    color_map = {
        "New with Tags": "#b5c99a",
        "Like New":      "#ffb7b2",
        "Gently Used":   "#d4a373",
        "Well-Loved":    "#802b2b",
        "Flawed":        "#5d1a1a"
    }
    sticker_color = color_map.get(condition, "#802b2b")
    text_color = "white"

    return f"""
    <div class="hang-tag">
        <div style="text-align:center; margin-bottom:6px;">
            <span style="background:{sticker_color}; color:{text_color};
                padding:5px 14px; border-radius:20px; font-size:11px;
                font-family:'Gaegu',cursive; font-weight:700;
                letter-spacing:0.08em; display:inline-block;">
                {condition.upper()}
            </span>
        </div>
        <h2 style="text-align:center; font-size:32px !important; margin:6px 0 2px;">{brand.upper()}</h2>
        <p style="text-align:center; font-style:italic; margin:0 0 10px; font-size:16px !important;">{item_type}</p>
        <div style="border-top: 2px dashed #802b2b; margin: 12px 0;"></div>
        <div style="text-align:center; font-family:'Gaegu',cursive;
            font-size:64px; font-weight:700; color:#802b2b;
            line-height:1; margin:8px 0;">${price:.2f}</div>
        <div style="border-top: 2px dashed #d4a373; margin: 12px 0;"></div>
        <p style="text-align:center; font-size:11px !important;
            color:#aaa !important; margin:0; font-family:'Courier New',monospace;">
            stitch &amp; scout · priced with ✦ care
        </p>
    </div>
    """


def scrapbook_entry_html(item_name, price, date):
    return f"""
    <div style="
        background-color: #fdfaf0;
        border: 1px solid #d4a373;
        padding: 10px 12px;
        margin-bottom: 12px;
        border-radius: 4px;
        box-shadow: 2px 2px 0px #d4a373;
        font-family: 'Courier New', Courier, monospace;
        position: relative;
    ">
        <div style="
            position: absolute;
            top: -7px; left: 50%;
            transform: translateX(-50%);
            width: 44px; height: 14px;
            background: rgba(255, 183, 178, 0.5);
            border: 1px dashed rgba(212,163,115,0.6);
            border-radius: 2px;
        "></div>
        <div style="font-size:11px; color:#802b2b; font-weight:bold; margin-top:4px;">{date}</div>
        <div style="font-size:14px; color:#333; margin:4px 0 2px;">{item_name.upper()}</div>
        <div style="font-size:18px; color:#802b2b; text-align:right; font-weight:bold;">{price}</div>
    </div>
    """