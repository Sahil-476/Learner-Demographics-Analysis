import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px

# Curated High-Vibrancy Neon / Cyber Palette for maximum visual attraction
COLOR_PALETTE = [
    '#00F2FE',  # Electric Cyber Cyan
    '#FF0844',  # Luminous Neon Red/Pink
    '#00FF87',  # Vivid Mint Emerald
    '#FFB199',  # Warm Peach Coral
    '#7F00FF',  # Electric Amethyst Purple
    '#F857A6',  # Bright Magenta
    '#4FACFE',  # Sky Blue Glow
    '#FEE140',  # Vibrant Gold Amber
    '#00CDAC',  # Turquoise Mint
    '#FF007F'   # Hot Neon Pink
]

GENDER_COLORS = {
    'Female': '#FF007F', # Hot Neon Pink
    'Male': '#00F2FE',   # Cyber Cyan
    'Other': '#00FF87'   # Vivid Mint
}

AGE_COLORS = {
    '<18': '#00FF87',    # Mint
    '18-25': '#00F2FE',  # Cyan
    '26-35': '#7F00FF',  # Amethyst Purple
    '36-45': '#FF007F',  # Hot Pink
    '45+': '#FFB199'     # Coral Peach
}

LEVEL_COLORS = {
    'Beginner': '#00FF87',   # Vivid Mint
    'Intermediate': '#00F2FE', # Cyber Cyan
    'Advanced': '#FF0844'    # Neon Red
}

TYPE_COLORS = {
    'Free': '#00FF87',   # Vivid Mint
    'Paid': '#7F00FF'    # Electric Purple
}

def inject_custom_css(theme="dark"):
    """
    Injects ultra-modern, hyper-vibrant CSS into Streamlit for a luminous UI with
    glassmorphism, rainbow borders, glowing KPI cards, animated multi-gradient backgrounds,
    staggered section loading, hover lift cards, hover glow buttons, and dark/light mode adaptability.
    """
    is_light = (theme == "light")
    
    # Theme color definitions
    bg_gradient = (
        "linear-gradient(to right, rgba(0, 0, 0, 0.04) 1px, transparent 1px), linear-gradient(to bottom, rgba(0, 0, 0, 0.04) 1px, transparent 1px), linear-gradient(-45deg, #f8fafc, #e2e8f0, #cbd5e1, #f1f5f9)"
        if is_light else
        "linear-gradient(to right, rgba(255, 255, 255, 0.035) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.035) 1px, transparent 1px), linear-gradient(-45deg, #0f172a, #1e1b4b, #2a0845, #0f172a)"
    )
    text_color = "#0f172a" if is_light else "#f8fafc"
    card_bg = "rgba(255, 255, 255, 0.82)" if is_light else "rgba(30, 41, 59, 0.65)"
    card_border = "rgba(0, 0, 0, 0.12)" if is_light else "rgba(255, 255, 255, 0.18)"
    card_shadow = "0 10px 30px 0 rgba(0, 0, 0, 0.1)" if is_light else "0 10px 30px 0 rgba(0, 0, 0, 0.3)"
    heading_color = "#0f172a" if is_light else "#ffffff"
    subtext_color = "#475569" if is_light else "#cbd5e1"
    tab_list_bg = "rgba(241, 245, 249, 0.9)" if is_light else "rgba(15, 23, 42, 0.8)"
    sidebar_bg = "linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%)" if is_light else "linear-gradient(180deg, #0f172a 0%, #1e1b4b 100%)"

    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

        /* Keyframe Animations */
        @keyframes fadeInSlideUp {{
            0% {{ opacity: 0; transform: translateY(25px) scale(0.98); }}
            100% {{ opacity: 1; transform: translateY(0) scale(1); }}
        }}

        @keyframes heroEntrance {{
            0% {{ opacity: 0; transform: perspective(1000px) rotateX(12deg) translateY(-35px) scale(0.94); }}
            100% {{ opacity: 1; transform: perspective(1000px) rotateX(0deg) translateY(0) scale(1); }}
        }}

        @keyframes pulseGlow {{
            0%, 100% {{ box-shadow: 0 4px 20px rgba(0, 242, 254, 0.25), 0 0 10px rgba(255, 0, 127, 0.15); }}
            50% {{ box-shadow: 0 8px 35px rgba(255, 0, 127, 0.55), 0 0 25px rgba(0, 242, 254, 0.45); }}
        }}

        @keyframes gradientMove {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes bgShift {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        @keyframes floatUpDown {{
            0%, 100% {{ transform: translateY(0px); }}
            50% {{ transform: translateY(-8px); }}
        }}

        @keyframes borderShimmer {{
            0% {{ border-color: rgba(0, 242, 254, 0.4); }}
            50% {{ border-color: rgba(255, 0, 127, 0.8); }}
            100% {{ border-color: rgba(0, 242, 254, 0.4); }}
        }}

        @keyframes textShimmer {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}

        /* Premium Chart Animation Keyframes */
        @keyframes pieSpinDraw {{
            0% {{ transform: scale(0.85) rotate(-45deg); opacity: 0; }}
            100% {{ transform: scale(1) rotate(0deg); opacity: 1; }}
        }}

        @keyframes barGrowUp {{
            0% {{ transform: scaleY(0.4); opacity: 0; transform-origin: bottom; }}
            100% {{ transform: scaleY(1); opacity: 1; transform-origin: bottom; }}
        }}

        /* Loading Skeleton Keyframes */
        @keyframes skeletonShimmer {{
            0% {{ background-position: -200% 0; }}
            100% {{ background-position: 200% 0; }}
        }}

        /* Root styling - Vibrant Aurora Grid & Multi-Gradient Theme */
        /* Ensure smooth native scrolling across Streamlit view containers */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
            overflow-y: auto !important;
            overflow-x: hidden !important;
        }}

        html, body, .stApp {{
            font-family: 'Inter', sans-serif;
            background-image: {bg_gradient} !important;
            background-size: 45px 45px, 45px 45px, 100% 100% !important;
            color: {text_color} !important;
        }}

        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
            color: {heading_color} !important;
        }}

        /* App container */
        .block-container {{
            padding-top: 2rem !important;
            padding-bottom: 3.5rem !important;
            max-width: 1400px !important;
        }}

        /* Custom Header Title - Electric Luminous Multi-Color Shimmer */
        .main-title {{
            background: linear-gradient(270deg, #00f2fe, #ff007f, #00ff87, #7f00ff, #00f2fe);
            background-size: 300% 300%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 3rem;
            font-weight: 800;
            margin-bottom: 0.4rem;
            font-family: 'Outfit', sans-serif;
            animation: textShimmer 5s ease infinite;
            text-shadow: 0 0 35px rgba(0, 242, 254, 0.35);
        }}

        .sub-title {{
            color: {subtext_color};
            font-size: 1.2rem;
            margin-bottom: 2.2rem;
            font-weight: 400;
            letter-spacing: 0.01em;
        }}

        /* Glassmorphism Card Container - Vibrant Contrast & Mouse Spotlight */
        .glass-card {{
            background: {card_bg};
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid {card_border};
            border-radius: 18px;
            padding: 1.6rem;
            margin-bottom: 1.5rem;
            box-shadow: {card_shadow};
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            animation: fadeInSlideUp 0.5s ease forwards;
            position: relative;
            overflow: hidden;
        }}

        /* Mouse Spotlight Glow Overlay */
        .glass-card::before, [data-testid="stVerticalBlockBorderWrapper"]::before, .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: radial-gradient(600px circle at var(--mouse-x, 50%) var(--mouse-y, 50%), rgba(0, 242, 254, 0.12), transparent 40%);
            z-index: 0;
            pointer-events: none;
            opacity: 0;
            transition: opacity 0.3s ease;
        }}

        .glass-card:hover::before, [data-testid="stVerticalBlockBorderWrapper"]:hover::before, .kpi-card:hover::before {{
            opacity: 1;
        }}

        /* Hover Lift Cards Effect - Clean 2D Lift without perspective clipping */
        .glass-card:hover {{
            transform: translateY(-6px) !important;
            border-color: #00f2fe !important;
            box-shadow: 0 16px 35px rgba(0, 242, 254, 0.28), 0 0 25px rgba(255, 0, 127, 0.18) !important;
        }}

        /* Streamlit Native Containers styled as Vibrant Glass Cards */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background: {card_bg} !important;
            backdrop-filter: blur(20px) !important;
            border: 1px solid {card_border} !important;
            border-radius: 18px !important;
            padding: 1.1rem !important;
            box-shadow: {card_shadow} !important;
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.3s ease, border-color 0.3s ease !important;
            animation: fadeInSlideUp 0.6s ease forwards;
            position: relative;
        }}

        [data-testid="stVerticalBlockBorderWrapper"]:hover {{
            transform: translateY(-6px) !important;
            border-color: #00f2fe !important;
            box-shadow: 0 16px 35px rgba(0, 242, 254, 0.28), 0 0 25px rgba(127, 0, 255, 0.22) !important;
        }}

        /* Staggered Section Loading */
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(1) {{ animation-delay: 0.05s; }}
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(2) {{ animation-delay: 0.12s; }}
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(3) {{ animation-delay: 0.19s; }}
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(4) {{ animation-delay: 0.26s; }}
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(5) {{ animation-delay: 0.33s; }}
        [data-testid="stVerticalBlockBorderWrapper"]:nth-child(6) {{ animation-delay: 0.40s; }}

        /* Vibrant KPI Metric Cards */
        .kpi-card {{
            background: { "linear-gradient(135deg, rgba(255,255,255,0.9) 0%, rgba(241,245,249,0.95) 100%)" if is_light else "linear-gradient(135deg, rgba(30, 41, 59, 0.9) 0%, rgba(42, 8, 69, 0.85) 100%)" };
            border-radius: 18px;
            padding: 1.4rem;
            position: relative;
            overflow: hidden;
            border: 1px solid {card_border};
            border-left: 5px solid #00F2FE;
            box-shadow: {card_shadow};
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
            animation: fadeInSlideUp 0.5s ease forwards;
        }}

        .kpi-card:hover {{
            transform: translateY(-10px) scale(1.035) perspective(1000px) rotateX(2deg) !important;
            border-left: 5px solid #FF007F !important;
            border-color: rgba(255, 0, 127, 0.8) !important;
            box-shadow: 0 22px 45px rgba(255, 0, 127, 0.45), 0 0 30px rgba(0, 242, 254, 0.35) !important;
        }}

        .kpi-icon {{
            font-size: 2.6rem;
            position: absolute;
            right: 1.25rem;
            top: 1.25rem;
            opacity: 0.95;
            transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            animation: floatUpDown 4s ease-in-out infinite;
            z-index: 1;
        }}

        .kpi-card:hover .kpi-icon {{
            transform: scale(1.25) rotate(12deg);
        }}

        .kpi-title {{
            color: {subtext_color};
            font-size: 0.88rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            margin-bottom: 0.5rem;
            position: relative;
            z-index: 1;
        }}

        .kpi-value {{
            background: linear-gradient(90deg, { "#0f172a" if is_light else "#ffffff" }, #00f2fe, #ff007f);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.4rem;
            font-weight: 800;
            font-family: 'Outfit', sans-serif;
            margin-bottom: 0.3rem;
            animation: gradientMove 5s ease infinite;
            position: relative;
            z-index: 1;
        }}

        .kpi-subtitle {{
            color: #00ff87;
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.02em;
            position: relative;
            z-index: 1;
        }}

        /* Streamlit Tabs - Vibrant Neon Customization with Smooth Page Transitions */
        [data-testid="stTabContent"] {{
            animation: fadeInSlideUp 0.5s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 12px;
            background-color: {tab_list_bg};
            padding: 10px;
            border-radius: 16px;
            border: 1px solid {card_border};
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 46px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 12px;
            color: {subtext_color};
            font-weight: 600;
            padding: 0 22px;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }}

        .stTabs [data-baseweb="tab"]:hover {{
            color: {heading_color};
            background-color: rgba(127, 0, 255, 0.08);
            transform: translateY(-2px);
        }}

        .stTabs [aria-selected="true"] {{
            background: linear-gradient(135deg, #FF007F 0%, #7F00FF 50%, #00F2FE 100%) !important;
            background-size: 200% 200% !important;
            animation: gradientMove 4s ease infinite !important;
            color: #ffffff !important;
            border: 1px solid rgba(0, 242, 254, 0.8) !important;
            font-weight: 700 !important;
            box-shadow: 0 6px 25px rgba(255, 0, 127, 0.45), 0 0 15px rgba(0, 242, 254, 0.3) !important;
            transform: scale(1.02);
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"] {{
            background: {sidebar_bg} !important;
            border-right: 1px solid {card_border};
        }}

        /* Hover Glow Buttons (Neon Glow, Pulse, Ripple Click, Animated Gradient) */
        @keyframes buttonPulse {{
            0% {{ box-shadow: 0 0 15px rgba(0, 242, 254, 0.4), 0 0 5px rgba(255, 0, 127, 0.3); }}
            50% {{ box-shadow: 0 0 30px rgba(255, 0, 127, 0.7), 0 0 18px rgba(0, 255, 135, 0.5); }}
            100% {{ box-shadow: 0 0 15px rgba(0, 242, 254, 0.4), 0 0 5px rgba(255, 0, 127, 0.3); }}
        }}

        .stButton > button, .stDownloadButton > button, [data-testid="stBaseButton-secondary"] {{
            background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 30%, #7F00FF 60%, #FF007F 100%) !important;
            background-size: 300% 300% !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 14px !important;
            padding: 0.65rem 1.5rem !important;
            font-weight: 700 !important;
            transition: all 0.35s cubic-bezier(0.16, 1, 0.3, 1) !important;
            animation: gradientMove 4s ease infinite, buttonPulse 3s infinite !important;
            letter-spacing: 0.03em !important;
            cursor: pointer !important;
            position: relative;
            overflow: hidden;
        }}

        .stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stBaseButton-secondary"]:hover {{
            transform: translateY(-4px) scale(1.05) !important;
            box-shadow: 0 18px 40px rgba(255, 0, 127, 0.7), 0 0 35px rgba(0, 242, 254, 0.6) !important;
            border-color: #00ff87 !important;
        }}

        .stButton > button:active, .stDownloadButton > button:active {{
            transform: translateY(-1px) scale(0.98) !important;
        }}

        /* Dashboard Effects: Animated KPI Metric Values & Dataframes */
        [data-testid="stMetricValue"] {{
            background: linear-gradient(90deg, { "#0f172a" if is_light else "#ffffff" }, #00f2fe, #ff007f);
            background-size: 200% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800 !important;
            font-family: 'Outfit', sans-serif !important;
            animation: gradientMove 5s ease infinite !important;
        }}

        [data-testid="stDataFrame"] {{
            background-color: {card_bg};
            border-radius: 16px;
            border: 1px solid rgba(0, 242, 254, 0.25);
            box-shadow: {card_shadow};
            transition: all 0.4s ease;
        }}

        [data-testid="stDataFrame"]:hover {{
            border-color: #ff007f;
            box-shadow: 0 15px 35px rgba(255, 0, 127, 0.25), 0 0 20px rgba(0, 242, 254, 0.2);
            transform: translateY(-4px);
        }}

        /* Plotly Chart Container Animation (Pie Chart Drawing & Bar Growth) */
        [data-testid="stPlotlyChart"] {{
            animation: pieSpinDraw 0.7s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }}

        /* Loading Skeleton Box Styling */
        .loading-skeleton-box {{
            background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(0,242,254,0.2) 50%, rgba(255,255,255,0.05) 75%);
            background-size: 200% 100%;
            animation: skeletonShimmer 1.8s infinite linear;
            border-radius: 14px;
            height: 90px;
            margin-bottom: 1rem;
            border: 1px solid rgba(255,255,255,0.1);
        }}
    </style>
    """, unsafe_allow_html=True)

def inject_cursor_bubble():
    """
    Alias for backward compatibility. Directs to the comprehensive frontend engine.
    """
    inject_premium_frontend_engine()

def inject_premium_frontend_engine():
    """
    Injects 4 morphing gradient blobs, tsParticles interactive background canvas,
    and a robust JavaScript engine supporting GSAP, ScrollTrigger, Lenis smooth scrolling,
    CountUp.js number animations, AOS (Animate On Scroll), and Mouse Spotlight tracking.
    """
    # 1. Inject CSS for 4 organic morphing gradient blobs
    st.markdown("""
    <style>
        @keyframes blobMorph {
            0%, 100% { border-radius: 40% 60% 70% 30% / 40% 50% 60% 50%; transform: translate(0, 0) rotate(0deg) scale(1); }
            33% { border-radius: 70% 30% 50% 50% / 30% 30% 70% 70%; transform: translate(140px, -90px) rotate(120deg) scale(1.15); }
            66% { border-radius: 100% 60% 60% 100% / 100% 100% 60% 60%; transform: translate(-120px, 140px) rotate(240deg) scale(0.85); }
        }

        @keyframes floatOrb1 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(150px, -100px) scale(1.2); }
            66% { transform: translate(-100px, 150px) scale(0.85); }
        }

        @keyframes floatOrb2 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            33% { transform: translate(-150px, 150px) scale(0.9); }
            66% { transform: translate(120px, -120px) scale(1.15); }
        }

        .ambient-blob-1 {
            position: fixed; top: 5%; left: 5%; width: 480px; height: 480px;
            background: radial-gradient(circle, rgba(0, 242, 254, 0.22) 0%, rgba(127, 0, 255, 0.08) 50%, transparent 70%);
            border-radius: 50%; filter: blur(40px); z-index: 0; pointer-events: none;
            animation: blobMorph 24s ease-in-out infinite;
        }

        .ambient-blob-2 {
            position: fixed; bottom: 5%; right: 5%; width: 520px; height: 520px;
            background: radial-gradient(circle, rgba(255, 0, 127, 0.22) 0%, rgba(0, 255, 135, 0.08) 50%, transparent 70%);
            border-radius: 50%; filter: blur(45px); z-index: 0; pointer-events: none;
            animation: blobMorph 28s ease-in-out infinite reverse;
        }

        .ambient-blob-3 {
            position: fixed; top: 60%; left: 10%; width: 400px; height: 400px;
            background: radial-gradient(circle, rgba(0, 255, 135, 0.16) 0%, rgba(0, 205, 172, 0.05) 50%, transparent 70%);
            border-radius: 50%; filter: blur(50px); z-index: 0; pointer-events: none;
            animation: floatOrb1 22s ease-in-out infinite;
        }

        .ambient-blob-4 {
            position: fixed; top: 15%; right: 15%; width: 450px; height: 450px;
            background: radial-gradient(circle, rgba(127, 0, 255, 0.18) 0%, rgba(248, 87, 166, 0.06) 50%, transparent 70%);
            border-radius: 50%; filter: blur(45px); z-index: 0; pointer-events: none;
            animation: floatOrb2 25s ease-in-out infinite;
        }

        /* Custom Top-Right Fork & GitHub Badge */
        .custom-github-badge-container {
            position: fixed; top: 14px; right: 20px; z-index: 999999;
            display: flex; align-items: center; gap: 22px;
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .github-badge-btn {
            display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px;
            font-size: 0.85rem; font-weight: 600; line-height: 1.2;
            color: #ffffff !important; background: rgba(30, 41, 59, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.22); border-radius: 20px;
            text-decoration: none !important; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.35); transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
            cursor: pointer;
        }

        .github-badge-btn:hover {
            transform: translateY(-2px) scale(1.05); border-color: #00F2FE !important;
            box-shadow: 0 0 18px rgba(0, 242, 254, 0.5), 0 4px 20px rgba(255, 0, 127, 0.3); color: #00F2FE !important;
        }

        .fork-btn:hover {
            border-color: #FF007F !important;
            box-shadow: 0 0 18px rgba(255, 0, 127, 0.5), 0 4px 20px rgba(0, 242, 254, 0.3); color: #FF007F !important;
        }

        @media (max-width: 768px) {
            .custom-github-badge-container {
                position: static; margin-bottom: 15px; justify-content: flex-end;
            }
        }
    </style>
    <div class="ambient-blob-1"></div>
    <div class="ambient-blob-2"></div>
    <div class="ambient-blob-3"></div>
    <div class="ambient-blob-4"></div>
    """, unsafe_allow_html=True)

    # 2. Inject JS for GSAP, ScrollTrigger, Lenis, CountUp, AOS, tsParticles, and Mouse Spotlight
    js_code = """
    <script>
    const parentDoc = window.parent.document;
    const parentWin = window.parent;

    // A. Load External Libraries (Lenis, GSAP, AOS, tsParticles) safely via CDN
    function loadScript(src, callback) {
        if (!parentDoc.querySelector(`script[src="${src}"]`)) {
            const script = parentDoc.createElement('script');
            script.src = src;
            script.async = true;
            script.onload = callback;
            parentDoc.head.appendChild(script);
        } else if (callback) {
            callback();
        }
    }

    // Clean up any existing Lenis instance to restore native touchpad 2-finger and mouse wheel scrolling
    if (parentWin._lenisInstance) {
        try { parentWin._lenisInstance.destroy(); } catch(e) {}
        parentWin._lenisInstance = null;
    }

    // Load AOS (Animate On Scroll)
    if (!parentDoc.querySelector('link[href*="aos.css"]')) {
        const link = parentDoc.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css';
        parentDoc.head.appendChild(link);
    }
    loadScript('https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js', () => {
        if (parentWin.AOS) {
            parentWin.AOS.init({ duration: 800, once: false, mirror: true });
        }
    });

    // Load tsParticles for background starfield constellation
    loadScript('https://cdn.jsdelivr.net/npm/tsparticles-slim@2.12.0/tsparticles.slim.bundle.min.js', () => {
        if (parentWin.tsParticles && !parentDoc.getElementById('tsparticles-bg')) {
            const bgDiv = parentDoc.createElement('div');
            bgDiv.id = 'tsparticles-bg';
            bgDiv.style.cssText = 'position:fixed; top:0; left:0; width:100%; height:100%; z-index:0; pointer-events:none; opacity:0.6;';
            parentDoc.body.prepend(bgDiv);
            
            parentWin.tsParticles.load("tsparticles-bg", {
                fpsLimit: 60,
                particles: {
                    number: { value: 35, density: { enable: true, value_area: 800 } },
                    color: { value: ["#00F2FE", "#FF007F", "#00FF87"] },
                    shape: { type: "circle" },
                    opacity: { value: 0.5, random: true },
                    size: { value: { min: 1, max: 3 } },
                    links: { enable: true, distance: 150, color: "#00F2FE", opacity: 0.2, width: 1 },
                    move: { enable: true, speed: 0.8, direction: "none", random: false, straight: false, outModes: "out" }
                },
                detectRetina: true
            });
        }
    });

    // B. Interactive Cursor Tracking Bubble with 0-latency instant sync
    if (!parentDoc.getElementById('cursor-glow-bubble')) {
        const bubble = parentDoc.createElement('div');
        bubble.id = 'cursor-glow-bubble';
        bubble.style.cssText = `
            position: fixed; top: 0; left: 0; width: 340px; height: 340px; border-radius: 50%;
            background: radial-gradient(circle, rgba(0, 242, 254, 0.22) 0%, rgba(255, 0, 127, 0.15) 45%, rgba(0, 0, 0, 0) 70%);
            pointer-events: none; z-index: 99999;
            transition: transform 0.05s linear, background 0.3s ease;
            filter: blur(20px); opacity: 0.95;
            transform: translate3d(-500px, -500px, 0);
        `;
        parentDoc.body.appendChild(bubble);
        
        parentDoc.addEventListener('mousemove', (e) => {
            bubble.style.transform = `translate3d(${e.clientX - 170}px, ${e.clientY - 170}px, 0)`;
        }, { passive: true });

        parentDoc.addEventListener('mousedown', () => {
            bubble.style.background = 'radial-gradient(circle, rgba(255, 0, 127, 0.40) 0%, rgba(0, 255, 135, 0.30) 45%, rgba(0, 0, 0, 0) 70%)';
        });

        parentDoc.addEventListener('mouseup', () => {
            bubble.style.background = 'radial-gradient(circle, rgba(0, 242, 254, 0.22) 0%, rgba(255, 0, 127, 0.15) 45%, rgba(0, 0, 0, 0) 70%)';
        });
    }

    // C. Scroll-Triggered Progress Bar (Glowing Top Progress Bar)
    if (!parentDoc.getElementById('scroll-progress-indicator')) {
        const progressBar = parentDoc.createElement('div');
        progressBar.id = 'scroll-progress-indicator';
        progressBar.style.cssText = `
            position: fixed; top: 0; left: 0; height: 4px; width: 0%;
            background: linear-gradient(90deg, #00F2FE, #00FF87, #7F00FF, #FF007F, #00F2FE);
            background-size: 300% 100%; z-index: 999999; transition: width 0.1s ease-out;
            box-shadow: 0 0 15px #00F2FE, 0 0 25px #FF007F;
        `;
        parentDoc.body.appendChild(progressBar);
        
        parentDoc.addEventListener('scroll', () => {
            const scrollTop = parentDoc.documentElement.scrollTop || parentDoc.body.scrollTop;
            const scrollHeight = (parentDoc.documentElement.scrollHeight || parentDoc.body.scrollHeight) - parentDoc.documentElement.clientHeight;
            const progress = scrollHeight > 0 ? (scrollTop / scrollHeight) * 100 : 0;
            progressBar.style.width = progress + '%';
        }, { passive: true });
    }

    // D. Mouse Spotlight Tracking optimized with RAF throttling for 60 FPS
    let spotlightRaf = null;
    parentDoc.addEventListener('mousemove', (e) => {
        if (spotlightRaf) return;
        spotlightRaf = requestAnimationFrame(() => {
            spotlightRaf = null;
            const cards = parentDoc.querySelectorAll('.glass-card, [data-testid="stVerticalBlockBorderWrapper"], .kpi-card');
            cards.forEach(card => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });
        });
    }, { passive: true });

    // E. High-Performance RAF Number CountUp Engine starting from 0
    function runCountUpAnimations() {
        try {
            const countElements = parentDoc.querySelectorAll('.kpi-value[data-countup]:not([data-counted="true"])');
            countElements.forEach(el => {
                el.setAttribute('data-counted', 'true');
                const targetStr = el.getAttribute('data-countup') || '0';
                const prefix = el.getAttribute('data-prefix') || '';
                const suffix = el.getAttribute('data-suffix') || '';
                const isPercent = targetStr.includes('%');
                const effectiveSuffix = suffix || (isPercent ? '%' : '');
                
                const rawNum = parseFloat(targetStr.replace(/[^0-9.-]/g, '')) || 0;
                
                let finalDisplay = targetStr;
                if (prefix && !finalDisplay.startsWith(prefix)) finalDisplay = prefix + finalDisplay;
                if (effectiveSuffix && !finalDisplay.endsWith(effectiveSuffix)) finalDisplay = finalDisplay + effectiveSuffix;
                
                let decimals = 0;
                const matchDec = targetStr.match(/[.]([0-9]+)/);
                if (matchDec) {
                    decimals = matchDec[1].length;
                }
                
                let startTime = null;
                const duration = 1400;
                
                function step(timestamp) {
                    if (!startTime) startTime = timestamp;
                    const progress = Math.min((timestamp - startTime) / duration, 1);
                    const easeOut = 1 - Math.pow(1 - progress, 3);
                    const currentVal = rawNum * easeOut;
                    
                    let formatted;
                    if (decimals > 0) {
                        formatted = currentVal.toFixed(decimals);
                    } else {
                        formatted = Math.floor(currentVal).toLocaleString();
                    }
                    
                    el.innerText = `${prefix}${formatted}${effectiveSuffix}`;
                    
                    if (progress < 1) {
                        requestAnimationFrame(step);
                    } else {
                        el.innerText = finalDisplay;
                    }
                }
                requestAnimationFrame(step);
            });
        } catch(err) {}
    }

    // Observe Streamlit DOM mutations so tab switches trigger count up from 0
    const observer = new MutationObserver(() => {
        runCountUpAnimations();
    });
    if (parentDoc.body) {
        observer.observe(parentDoc.body, { childList: true, subtree: true });
    }

    setInterval(runCountUpAnimations, 600);
    setTimeout(runCountUpAnimations, 150);

    // Instant zero-loop autoscale on first load and Tab Click for all Plotly charts
    function autoscaleAllChartsNow() {
        // 1. Resize all Plotly charts in main document
        parentDoc.querySelectorAll('.js-plotly-plot').forEach(function(plot) {
            if (parentWin.Plotly && typeof parentWin.Plotly.Plots.resize === 'function') {
                parentWin.Plotly.Plots.resize(plot);
            }
        });
        // 2. Resize all Streamlit iframed charts
        parentDoc.querySelectorAll('iframe').forEach(function(ifr) {
            try {
                const win = ifr.contentWindow;
                const doc = ifr.contentDocument || win.document;
                if (win) {
                    win.dispatchEvent(new Event('resize'));
                }
                if (win && doc) {
                    doc.querySelectorAll('.js-plotly-plot').forEach(function(plot) {
                        if (win.Plotly) {
                            if (typeof win.Plotly.Plots.resize === 'function') {
                                win.Plotly.Plots.resize(plot);
                            }
                            if (typeof win.Plotly.relayout === 'function') {
                                win.Plotly.relayout(plot, {autosize: true});
                            }
                        }
                    });
                }
            } catch(err) {}
        });
        try { parentWin.dispatchEvent(new Event('resize')); } catch(e) {}
    }

    function triggerAllAnimationsNow() {
        parentDoc.querySelectorAll('.kpi-value[data-countup]').forEach(el => {
            el.removeAttribute('data-counted');
        });
        runCountUpAnimations();
    }

    parentDoc.addEventListener('click', function(e) {
        const tabHeader = e.target.closest('[role="tab"], button[data-baseweb="tab"]');
        if (tabHeader) {
            setTimeout(autoscaleAllChartsNow, 30);
            setTimeout(autoscaleAllChartsNow, 120);
            setTimeout(autoscaleAllChartsNow, 300);
            setTimeout(autoscaleAllChartsNow, 600);
            setTimeout(triggerAllAnimationsNow, 50);
        }
    }, { passive: true });

    // Auto-trigger on initial page load across multiple intervals so charts load perfectly at 100% width
    setTimeout(autoscaleAllChartsNow, 100);
    setTimeout(autoscaleAllChartsNow, 350);
    setTimeout(autoscaleAllChartsNow, 700);
    setTimeout(autoscaleAllChartsNow, 1400);
    </script>
    """
    components.html(js_code, height=0, width=0)

def render_custom_github_badge():
    """
    Renders a custom floating Fork & GitHub repository badge in the top right corner.
    """
    badge_html = """
    <div class="custom-github-badge-container">
        <a href="https://github.com/Sahil-476/Learner-Demographics-Analysis/fork" target="_blank" class="github-badge-btn fork-btn" title="Fork repository on GitHub">
            <svg aria-hidden="true" height="15" viewBox="0 0 16 16" width="15" fill="currentColor" style="vertical-align: middle;">
                <path d="M5 5.372v.878c0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75v-.878a2.25 2.25 0 1 1 1.5 0v.878a2.25 2.25 0 0 1-2.25 2.25h-1.5v2.128a2.251 2.251 0 1 1-1.5 0V8.5h-1.5A2.25 2.25 0 0 1 3.5 6.25v-.878a2.25 2.25 0 1 1 1.5 0ZM5 3.25a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Zm6.75.75a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm-3 8.75a.75.75 0 1 0-1.5 0 .75.75 0 0 0 1.5 0Z"></path>
            </svg>
            <span>Fork</span>
        </a>
        <a href="https://github.com/Sahil-476/Learner-Demographics-Analysis" target="_blank" class="github-badge-btn repo-btn" title="View repository on GitHub">
            <svg aria-hidden="true" height="15" viewBox="0 0 16 16" width="15" fill="currentColor" style="vertical-align: middle;">
                <path d="M8 0c4.42 0 8 3.58 8 8 0 3.54-2.29 6.53-5.47 7.59-.4.07-.55-.17-.55-.38 0-.27.01-1.13.01-2.2 0-.75-.25-1.23-.54-1.48 1.78-.2 3.65-.88 3.65-3.95 0-.88-.31-1.59-.82-2.15.08-.2.36-1.02-.08-2.12 0 0-.67-.22-2.2.82-.64-.18-1.32-.27-2-.27-.68 0-1.36.09-2 .27-1.53-1.03-2.2-.82-2.2-.82-.44 1.1-.16 1.92-.08 2.12-.51.56-.82 1.28-.82 2.15 0 3.06 1.86 3.75 3.64 3.95-.23.2-.44.55-.51 1.07-.46.21-1.61.55-2.33-.66-.15-.24-.6-.83-1.23-.82-.67.01-.27.38.01.53.34.19.73.9.82 1.13.16.45.68 1.31 2.69.94 0 .67.01 1.3.01 1.49 0 .21-.15.45-.55.38A7.995 7.995 0 0 1 0 8c0-4.42 3.58-8 8-8Z"></path>
            </svg>
            <span>GitHub</span>
        </a>
    </div>
    """
    st.markdown(badge_html, unsafe_allow_html=True)

def render_header(title, subtitle=""):
    """
    Renders an electric modern header with Hero Intro Animation for the Streamlit app.
    """
    render_custom_github_badge()
    st.markdown(f'<div class="main-title" data-aos="fade-down">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="sub-title" data-aos="fade-up" data-aos-delay="150">{subtitle}</div>', unsafe_allow_html=True)

def render_kpi_card(title, value, subtitle="", icon="📊", prefix="", suffix="", **kwargs):
    """
    Renders an HTML/CSS styled KPI card with vibrant neon hover glow animation,
    Mouse Spotlight support, and CountUp data attributes for smooth number counting.
    """
    val_str = str(value)
    display_str = val_str
    if prefix and not display_str.startswith(prefix):
        display_str = f"{prefix}{display_str}"
    if suffix and not display_str.endswith(suffix):
        display_str = f"{display_str}{suffix}"

    html = f"""
    <div class="kpi-card" data-aos="zoom-in-up">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-title">{title}</div>
        <div class="kpi-value" data-countup="{val_str}" data-prefix="{prefix}" data-suffix="{suffix}">{display_str}</div>
        <div class="kpi-subtitle">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

def render_loading_skeleton(count=2):
    """
    Renders shimmering CSS loading skeletons for smooth state transitions.
    """
    skeleton_html = ""
    for _ in range(count):
        skeleton_html += '<div class="loading-skeleton-box"></div>'
    st.markdown(skeleton_html, unsafe_allow_html=True)

def render_footer():
    """
    Renders the custom animated LinkedIn footer requested by the user globally.
    """
    footer_html = """
    <div style="margin-top: 4rem; padding-top: 2rem; border-top: 1px solid rgba(128, 128, 128, 0.25); text-align: center; font-family: 'Inter', sans-serif; opacity: 1;">
        <p style="font-size: 1.15rem; font-weight: 700; margin-bottom: 0.4rem; letter-spacing: 0.02em;">
            Made with ❤️ by <a href="https://www.linkedin.com/in/sk-mahammad-sahil" target="_blank" style="color: #00F2FE; text-decoration: none; font-weight: 800; transition: all 0.3s ease; text-shadow: 0 0 15px rgba(0, 242, 254, 0.5);">Sahil</a>
        </p>
        <p style="font-size: 0.95rem; margin-top: 0; font-weight: 500; opacity: 0.75;">
            © 2026 Sahil. All rights reserved.
        </p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)

def get_plotly_layout(title="", height=420, show_legend=True, barmode=None, theme="dark"):
    """
    Returns a unified layout for Plotly charts with animated transitions and dynamic theme adaptability.
    """
    is_light = (theme == "light")
    font_color = "#0f172a" if is_light else "#cbd5e1"
    title_color = "#0f172a" if is_light else "#ffffff"
    grid_color = "rgba(0, 0, 0, 0.08)" if is_light else "rgba(255, 255, 255, 0.08)"
    zeroline_color = "rgba(0, 242, 254, 0.35)"
    hover_bg = "#ffffff" if is_light else "#0f172a"

    layout = dict(
        title=dict(
            text=f"<b>{title}</b>" if title else "",
            font=dict(size=17, color=title_color, family="Outfit, sans-serif"),
            x=0.02,
            y=0.95
        ),
        height=height,
        autosize=True,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color=font_color, family="Inter, sans-serif"),
        margin=dict(l=75, r=35, t=65, b=75),
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1.0,
            font=dict(size=12, color=title_color)
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zerolinecolor=zeroline_color,
            tickfont=dict(color=font_color, size=13),
            automargin=True
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=grid_color,
            zerolinecolor=zeroline_color,
            tickfont=dict(color=font_color),
            automargin=True
        ),
        hoverlabel=dict(
            bgcolor=hover_bg,
            bordercolor='#00f2fe',
            font_size=13,
            font_family="Inter, sans-serif"
        ),
        hovermode="closest"
    )
    if barmode:
        layout['barmode'] = barmode
    return layout
