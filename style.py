import streamlit as st

def apply_diy_theme():
    st.markdown("""
    <style>
    /* Import friendly, handwritten fonts */
    @import url('https://fonts.googleapis.com/css2?family=Gaegu:wght@400;700&family=Fira+Sans:wght@400;700&display=swap');
    
    /* Warm, layered scrapbook background */
    .stApp {
        background-color: #fdfaf0; /* Creamy paper base */
        background-image: radial-gradient(#d88b8b 1px, transparent 1px);
        background-size: 40px 40px; /* Subtle polka dots */
    }

    /* Scalloped Maroon Header Bar */
    h1 {
        font-family: 'Gaegu', cursive !important;
        background-color: #802b2b !important; /* Deep Maroon */
        color: #fce4ec !important; /* Soft Pink */
        padding: 20px;
        border-radius: 0 0 50px 50px;
        text-align: center;
        border-bottom: 5px solid #d4a373;
        box-shadow: 0 4px 0 #5d1a1a;
    }

    /* Subheaders and Labels */
    h2, h3, label, p {
        font-family: 'Gaegu', cursive !important;
        color: #5d1a1a !important;
        font-size: 22px !important;
    }

    /* Crafty Input Boxes */
    input, div[data-baseweb="select"] {
        background-color: #fff9f9 !important;
        border: 3px solid #d4a373 !important;
        border-radius: 15px !important;
        color: #5d1a1a !important;
    }

    /* 'Washi Tape' Style Buttons */
    .stButton>button {
        background-color: #b5c99a !important; /* Sage Green */
        color: #5d1a1a !important;
        border: none !important;
        border-bottom: 4px solid #869471 !important;
        border-radius: 0px !important;
        font-family: 'Gaegu', cursive;
        font-weight: 700;
        font-size: 24px;
        transform: rotate(-1deg); /* Slight tilt for DIY feel */
        transition: 0.2s;
    }

    .stButton>button:hover {
        transform: rotate(1deg) scale(1.05);
        background-color: #ffb7b2 !important; /* Coral Pink */
    }

    /* The Hang Tag: Scrapbook Card Style */
    .hang-tag {
        background: #fdfaf0;
        border: 4px solid #802b2b;
        padding: 30px;
        border-radius: 20px;
        position: relative;
        box-shadow: 10px 10px 0px #b5c99a; /* Sage shadow */
    }

    .hang-tag::before {
        content: "●"; /* Reinforcement hole */
        position: absolute;
        top: 10px;
        left: 50%;
        color: #802b2b;
    }
    </style>
    """, unsafe_allow_html=True)

def hang_tag_html(brand, item_type, price, condition):
    # Color code the condition stickers
    color_map = {
        "New with Tags": "#b5c99a", # Sage Green
        "Like New": "#ffb7b2",      # Coral Pink
        "Gently Used": "#d4a373",   # Tan
        "Well-Loved": "#802b2b",    # Maroon
        "Flawed": "#5d1a1a"         # Darker Maroon
    }
    sticker_color = color_map.get(condition, "#802b2b")

    return f"""
    <div class="hang-tag">
        <div style="background:{sticker_color}; color:white; padding:5px 10px; border-radius:15px; font-size:10px; display:inline-block; margin-bottom:10px;">
            {condition.upper()}
        </div>
        <h2 style="text-align:center; font-size:35px !important; margin:5px 0;">{brand.upper()}</h2>
        <p style="text-align:center; font-style:italic; margin-top:-5px;">{item_type}</p>
        <div style="border-top: 2px dashed #802b2b; margin: 15px 0;"></div>
        <h1 style="text-align:center; font-size:70px !important; color:#802b2b !important; padding:0;">${price:.2f}</h1>
    </div>
    """

def scrapbook_entry_html(item_name, price, date):
    return f"""
    <div style="
        background-color: #fdfaf0;
        border: 1px solid #d4a373;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
        font-family: 'Courier New', Courier, monospace;
        position: relative;
    ">
        <div style="
            position: absolute;
            top: -5px;
            left: 50%;
            transform: translateX(-50%);
            width: 40px;
            height: 15px;
            background: rgba(212, 163, 115, 0.3);
            border: 1px dashed rgba(212, 163, 115, 0.5);
        "></div>
        <div style="font-size: 12px; color: #802b2b; font-weight: bold;">{date}</div>
        <div style="font-size: 16px; color: #333; margin: 5px 0;">{item_name.upper()}</div>
        <div style="font-size: 20px; color: #802b2b; text-align: right; font-weight: bold;">{price}</div>
    </div>
    """